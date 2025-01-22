import unittest
from enum import Enum, auto

from fsmate import ImpossibleTransitionError, StateDescriptor
from fsmate._state import AttributeStateStorage, StateDispatcher
from unittest.mock import MagicMock, call


class State(Enum):
    A = auto()
    B = auto()
    C = auto()


class WrongState(Enum):
    D = auto()
    E = auto()
    F = auto()


class TestStateAttribute(unittest.TestCase):
    def setUp(self) -> None:
        class Stub:
            state = StateDescriptor(State, State.A)

        self.obj = Stub()

    def test_initital_state(self):
        self.assertEqual(self.obj.state, State.A)

    def test_forbid_state_direct_change(self):
        with self.assertRaisesRegex(
            AttributeError, 'Cannot change state directly. Use transitions'
        ):
            self.obj.state = State.B

    def test_default_attribute_change(self):
        with self.assertRaises(AttributeError):
            self.obj._state

        self.obj._state = State.B
        self.assertEqual(self.obj.state, State.B)

    def test_custom_atribute_change(self):
        class Stub:
            state_attribute: State = State.A
            state = StateDescriptor(State, state_storage=AttributeStateStorage('state_attribute'))

        obj = Stub()

        self.assertEqual(obj.state, State.A)

        obj.state_attribute = State.B
        self.assertEqual(obj.state, State.B)


class TestDeclareTransitions(unittest.TestCase):
    def test_destination_state_not_found(self):
        with self.assertRaisesRegex(ValueError, 'Destination state not found'):

            class _:
                state = StateDescriptor(State, State.A)
                to_d = state.transition(State.A, WrongState.D)

    def test_source_state_not_found(self):
        with self.assertRaisesRegex(ValueError, 'Source state not found'):

            class _:
                state = StateDescriptor(State, State.A)
                from_d_to_a = state.transition(WrongState.D, State.A)

    def test_one_of_sources_not_found(self):
        with self.assertRaisesRegex(ValueError, 'Source state not found'):

            class _:
                state = StateDescriptor(State, State.A)
                from_b_or_d_to_a = state.transition([State.B, WrongState.D], State.A)


class TestTransitions(unittest.TestCase):
    def setUp(self) -> None:
        class Stub:
            state = StateDescriptor(State, State.A)

            to_b = state.transition(State.A, State.B)
            to_c = state.transition(State.B, State.C)
            to_a_from_c = state.transition(State.C, State.A)
            to_b_from_a_or_c = state.transition([State.A, State.C], State.B)

        self.obj = Stub()

    def test_valid_transition(self):
        self.assertEqual(self.obj.state, State.A)
        self.obj.to_b()
        self.assertEqual(self.obj.state, State.B)

        self.obj.to_c()
        self.assertEqual(self.obj.state, State.C)

        self.obj.to_a_from_c()
        self.assertEqual(self.obj.state, State.A)

        self.obj.to_b_from_a_or_c()
        self.assertEqual(self.obj.state, State.B)

    def test_invalid_transition(self):
        with self.assertRaises(ImpossibleTransitionError):
            self.obj.to_c()

    def test_multiple_sources(self):
        self.obj.to_b_from_a_or_c()
        self.assertEqual(self.obj.state, State.B)

        self.obj._state = State.C
        self.obj.to_b_from_a_or_c()
        self.assertEqual(self.obj.state, State.B)

        self.obj._state = State.B
        with self.assertRaises(ImpossibleTransitionError):
            self.obj.to_b_from_a_or_c()


class TestMethodOverload(unittest.TestCase):
    def test_state_dispatcher(self):
        class StubStateStorage:
            def get_state(self, instance):
                return self.state

            def set_state(self, instance, state):
                self.state = state

        def fallback(x):
            return x

        def b_func(x):
            return x * 2

        storage = StubStateStorage()
        storage.state = State.A
        dispatcher = StateDispatcher(storage, State, fallback)
        dispatcher.register(b_func, State.B)

        self.assertEqual(dispatcher.dispatch(None, 10), 10)
        storage.set_state(None, State.B)
        self.assertEqual(dispatcher.dispatch(None, 10), 20)
        storage.set_state(None, State.C)
        self.assertEqual(dispatcher.dispatch(None, 10), 10)

        with self.assertRaisesRegex(ValueError, 'Target state not found'):
            dispatcher.register(lambda x: x, WrongState.D)

        with self.assertRaisesRegex(ValueError, 'Function is already overloaded for state'):
            dispatcher.register(lambda x: x, State.B)

    def test_overload(self):
        class Stub:
            state = StateDescriptor(State, State.A)

            to_b = state.transition(State.A, State.B)
            to_c = state.transition(State.B, State.C)

            @state.dispatch
            def foo(self):
                return 0

            @foo.overload(State.B)
            def _(self):
                return 1

        obj = Stub()

        self.assertEqual(obj.foo(), 0)

        obj.to_b()
        self.assertEqual(obj.foo(), 1)

        obj.to_c()
        self.assertEqual(obj.foo(), 0)


class TestCallbacks(unittest.TestCase):
    def test_transition_callbacks(self) -> None:
        callback_mock = MagicMock()

        class Stub:
            state = StateDescriptor(State, State.A)

            to_b = state.transition(State.A, State.B)
            to_c = state.transition(State.B, State.C)
            to_a = state.transition([State.B, State.C], State.A)

            @state.on_transition(to_b)  # type: ignore
            def on_to_b(self, from_state: State, to_state: State) -> None:
                callback_mock('to_b', self, from_state, to_state)

            @state.on_transition(to_c)  # type: ignore
            def on_to_c(self, from_state: State, to_state: State) -> None:
                callback_mock('to_c', self, from_state, to_state)

            @state.on_transition(to_a)  # type: ignore
            def on_to_a(self, from_state: State, to_state: State) -> None:
                callback_mock('to_a', self, from_state, to_state)

            @state.on_transition(to_b, to_c)  # type: ignore
            def on_to_b_to_c(self, from_state: State, to_state: State):
                callback_mock('to_b_to_c', self, from_state, to_state)

            @state.on_transition  # type: ignore
            def on_to_any(self, from_state: State, to_state: State) -> None:
                callback_mock('to_any', self, from_state, to_state)

        obj = Stub()

        obj.to_b()
        callback_mock.assert_has_calls(
            [
                call('to_b', obj, State.A, State.B),
                call('to_b_to_c', obj, State.A, State.B),
                call('to_any', obj, State.A, State.B),
            ]
        )
        callback_mock.reset_mock()

        obj.to_c()
        callback_mock.assert_has_calls(
            [
                call('to_c', obj, State.B, State.C),
                call('to_b_to_c', obj, State.B, State.C),
                call('to_any', obj, State.B, State.C),
            ]
        )
        callback_mock.reset_mock()

        obj.to_a()
        callback_mock.assert_has_calls(
            [
                call('to_a', obj, State.C, State.A),
                call('to_any', obj, State.C, State.A),
            ]
        )
        callback_mock.reset_mock()

        obj.to_b()
        callback_mock.assert_has_calls(
            [
                call('to_b', obj, State.A, State.B),
                call('to_b_to_c', obj, State.A, State.B),
                call('to_any', obj, State.A, State.B),
            ]
        )
        callback_mock.reset_mock()

        obj.to_a()
        callback_mock.assert_has_calls(
            [
                call('to_a', obj, State.B, State.A),
                call('to_any', obj, State.B, State.A),
            ]
        )

    def test_enter_state_callbaks(self):
        callback_mock = MagicMock()

        class Stub:
            state = StateDescriptor(State, State.A)

            to_b = state.transition(State.A, State.B)
            to_c = state.transition(State.B, State.C)
            to_a = state.transition([State.B, State.C], State.A)

            @state.on_state_entered(State.A)  # type: ignore
            def on_a_entered(self, from_state: State, to_state: State):
                callback_mock('A_entered', self, from_state, to_state)

            @state.on_state_entered(State.B)  # type: ignore
            def on_b_entered(self, from_state: State, to_state: State):
                callback_mock('B_entered', self, from_state, to_state)

            @state.on_state_entered(State.C)  # type: ignore
            def on_c_entered(self, from_state: State, to_state: State):
                callback_mock('C_entered', self, from_state, to_state)

            @state.on_state_entered  # type: ignore
            def on_any_entered(self, from_state: State, to_state: State):
                callback_mock('any_entered', self, from_state, to_state)

            @state.on_state_entered(State.A, State.B)  # type: ignore
            def on_a_b_entered(self, from_state: State, to_state: State):
                callback_mock('AB_entered', self, from_state, to_state)

        obj = Stub()

        obj.to_b()
        callback_mock.assert_has_calls(
            [
                call('any_entered', obj, State.A, State.B),
                call('B_entered', obj, State.A, State.B),
                call('AB_entered', obj, State.A, State.B),
            ],
            any_order=True,
        )
        callback_mock.reset_mock()

        obj.to_c()
        callback_mock.assert_has_calls(
            [
                call('any_entered', obj, State.B, State.C),
                call('C_entered', obj, State.B, State.C),
            ],
            any_order=True,
        )
        callback_mock.reset_mock()

        obj.to_a()
        callback_mock.assert_has_calls(
            [
                call('any_entered', obj, State.C, State.A),
                call('AB_entered', obj, State.C, State.A),
                call('A_entered', obj, State.C, State.A),
            ],
            any_order=True,
        )
        callback_mock.reset_mock()

        obj.to_b()
        callback_mock.assert_has_calls(
            [
                call('any_entered', obj, State.A, State.B),
                call('B_entered', obj, State.A, State.B),
                call('AB_entered', obj, State.A, State.B),
            ],
            any_order=True,
        )
        callback_mock.reset_mock()

        obj.to_a()
        callback_mock.assert_has_calls(
            [
                call('AB_entered', obj, State.B, State.A),
                call('A_entered', obj, State.B, State.A),
                call('any_entered', obj, State.B, State.A),
            ],
            any_order=True,
        )

    def test_exit_state_callbaks(self):
        callback_mock = MagicMock()

        class Stub:
            state = StateDescriptor(State, State.A)

            to_b = state.transition(State.A, State.B)
            to_c = state.transition(State.B, State.C)
            to_a = state.transition([State.B, State.C], State.A)

            @state.on_state_exited(State.A)  # type: ignore
            def on_a_exited(self, from_state: State, to_state: State):
                callback_mock('A_exited', self, from_state, to_state)

            @state.on_state_exited(State.B)  # type: ignore
            def on_b_exited(self, from_state: State, to_state: State):
                callback_mock('B_exited', self, from_state, to_state)

            @state.on_state_exited(State.C)  # type: ignore
            def on_c_exited(self, from_state: State, to_state: State):
                callback_mock('C_exited', self, from_state, to_state)

            @state.on_state_exited  # type: ignore
            def on_any_exited(self, from_state: State, to_state: State):
                callback_mock('any_exited', self, from_state, to_state)

            @state.on_state_exited(State.A, State.B)  # type: ignore
            def on_a_b_exited(self, from_state: State, to_state: State):
                callback_mock('AB_exited', self, from_state, to_state)

        obj = Stub()

        obj.to_b()
        callback_mock.assert_has_calls(
            [
                call('any_exited', obj, State.A, State.B),
                call('A_exited', obj, State.A, State.B),
                call('AB_exited', obj, State.A, State.B),
            ],
            any_order=True,
        )
        callback_mock.reset_mock()

        obj.to_c()
        callback_mock.assert_has_calls(
            [
                call('any_exited', obj, State.B, State.C),
                call('B_exited', obj, State.B, State.C),
            ],
            any_order=True,
        )
        callback_mock.reset_mock()

        obj.to_a()
        callback_mock.assert_has_calls(
            [
                call('any_exited', obj, State.C, State.A),
                call('C_exited', obj, State.C, State.A),
            ],
            any_order=True,
        )
        callback_mock.reset_mock()

        obj.to_b()
        callback_mock.assert_has_calls(
            [
                call('any_exited', obj, State.A, State.B),
                call('A_exited', obj, State.A, State.B),
                call('AB_exited', obj, State.A, State.B),
            ],
            any_order=True,
        )
        callback_mock.reset_mock()

        obj.to_a()
        callback_mock.assert_has_calls(
            [
                call('AB_exited', obj, State.B, State.A),
                call('B_exited', obj, State.B, State.A),
                call('any_exited', obj, State.B, State.A),
            ],
            any_order=True,
        )
