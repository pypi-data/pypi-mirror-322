from famegui.models import Observable
import unittest


class Observer:
    notified_count = 0

    def __init__(self, observable: Observable):
        observable.attach(self.notified)

    def notified(self) -> None:
        self.notified_count += 1


class TestObservable(unittest.TestCase):
    def test_subscription(self):
        event = Observable()
        event.notify()  # notifying an empty observable should have no effect

        # attach an observer
        obs1 = Observer(event)
        self.assertEqual(obs1.notified_count, 0)

        # simple notification
        event.notify()
        self.assertEqual(obs1.notified_count, 1)
        event.notify()
        self.assertEqual(obs1.notified_count, 2)

        # attach twice the same observer
        event.attach(obs1.notified)
        self.assertEqual(obs1.notified_count, 2)

        # should get double notification
        event.notify()
        self.assertEqual(obs1.notified_count, 4)

        # attach another observer
        obs2 = Observer(event)
        self.assertEqual(obs1.notified_count, 4)
        self.assertEqual(obs2.notified_count, 0)

        # notify all observers
        event.notify()
        self.assertEqual(obs1.notified_count, 6)
        self.assertEqual(obs2.notified_count, 1)

    def test_forwarding(self):
        event1 = Observable()
        event2 = Observable()
        obs = Observer(event2)

        event2.notify()
        self.assertEqual(obs.notified_count, 1)

        event1.notify()  # no effect
        self.assertEqual(obs.notified_count, 1)

        event2.forward(event1)
        event1.notify()
        self.assertEqual(obs.notified_count, 2)

        event2.notify()
        self.assertEqual(obs.notified_count, 3)

    def test_composition(self):
        class Property:
            def __init__(self):
                self.event = Observable()
                self._children = []

            def add_child(self, child: "Property") -> None:
                self._children.append(child)
                # propagate the event of the child
                self.event.forward(child.event)

        # create a tree of properties [p3->p2->p1]
        p1 = Property()
        p2 = Property()
        p3 = Property()
        p2.add_child(p1)
        p3.add_child(p2)

        # observe each property
        obs1 = Observer(p1.event)
        obs2 = Observer(p2.event)
        obs3 = Observer(p3.event)

        # test event propagation (notification forwarding)
        p1.event.notify()
        self.assertEqual(obs1.notified_count, 1)
        self.assertEqual(obs2.notified_count, 1)
        self.assertEqual(obs2.notified_count, 1)

        p2.event.notify()
        self.assertEqual(obs1.notified_count, 1)
        self.assertEqual(obs2.notified_count, 2)
        self.assertEqual(obs2.notified_count, 2)

        p3.event.notify()
        self.assertEqual(obs1.notified_count, 1)
        self.assertEqual(obs2.notified_count, 2)
        self.assertEqual(obs3.notified_count, 3)

        p2.event.notify()
        self.assertEqual(obs1.notified_count, 1)
        self.assertEqual(obs2.notified_count, 3)
        self.assertEqual(obs3.notified_count, 4)

        p1.event.notify()
        self.assertEqual(obs1.notified_count, 2)
        self.assertEqual(obs2.notified_count, 4)
        self.assertEqual(obs3.notified_count, 5)
