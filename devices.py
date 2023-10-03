# This module contains the classes which will manage the propagations and alerts
# for all the devices. It takes the output from read_file's append_contents function
# to sort the alerts and cancellations of the devices.


class TimeLine:
    """Creates a timeline of both alert and cancel events
    and sorts and removes the propagated according to their respective numbers"""
    def __init__(self, events: list, length: int, device_dict: dict):
        self.device_dict = device_dict
        self.limit = length
        self.time = events

    def _prop_event(self, event) -> None:
        """Takes in an event object either Alert or Cancel
        Checks what event it is and will propagate either a cancel or alert event.
        It will then print out the respective event and where it sent the event too.
        Once we reach the end, the innate timeline attributes is sorted."""

        if type(event) == CancelEvent:
            if event.get_sending_device() != -1:
                self.device_dict[event.get_receiving_device()].cancel(event.get_description())

        for delay, device in self.device_dict[event.get_receiving_device()].get_propagations():
            if self.device_dict[device].is_cancelled(event.get_description()):
                continue

            if type(event) == CancelEvent:
                self.time.append(CancelEvent(event.get_time() + delay, event.get_receiving_device(),
                                             device, event.get_description()))
                print(f"@{event.get_time()}: #{event.get_receiving_device()} SENT CANCELLATION TO #{device}: {event.get_description()}")

            else:
                self.time.append(AlertEvent(event.get_time() + delay, event.get_receiving_device(),
                                            device, event.get_description()))
                print(
                    f"@{event.get_time()}: #{event.get_receiving_device()} SENT ALERT TO #{device}: {event.get_description()}")

        self.time.sort()
    def pop_event(self):
        '''Returns topmost valid event from the stack of timelines, then prints depending on what type of event it is'''
        while True:
            if not self.time:
                return None
            event = self.time.pop(0)
            if not self.device_dict[event.get_receiving_device()].is_cancelled(event.event_description):
                break
        if event.time >= self.limit:
            return None
        result = event
        if result.get_sending_device() == -1:
            pass
        elif type(result) == CancelEvent:
            print(f'@{result.get_time()}: #{result.get_receiving_device()} RECEIVED CANCELLATION FROM #{result.get_sending_device()}: {result.get_description()}')
        else:
            print(
                f'@{result.get_time()}: #{result.get_receiving_device()} RECEIVED ALERT FROM #{result.get_sending_device()}: {result.get_description()}')
        self._prop_event(event)
        return event


class Event:
    """Contains getter methods for events."""
    def __init__(self, time: int, sending_device, receiving_device, event_description: str):
        self.time = time
        self.sending_device = sending_device
        self.receiving_device = receiving_device
        self.event_description = event_description

    #Getter Methods
    def get_time(self):
        return self.time

    def get_description(self):
        return self.event_description

    def get_receiving_device(self):
        return self.receiving_device

    def get_sending_device(self):
        return self.sending_device

    # def comes_before(self, other):
    #     '''If a certain events time comes before the other events time'''
    #     return self < other and self.get_description() == other.get_description()

    def __lt__(self, other):
        """Overrides the lt operator to compare the times of the objects"""
        return self.get_time() < other.get_time()

    def __eq__(self, other):
        """Overrides the time to set eq to another event object"""
        return self.get_time() == other.get_time()

    def __str__(self):
        """To print the object"""
        return str(self.sending_device) + " SENDING " + self.event_description + " to " + str(self.receiving_device) \
     + " AT " + str(self.time)


class AlertEvent(Event):
    """Creates an instance of an alert event."""
    def __init__(self, time: int, sending_device, receiving_device, event_description):
        Event.__init__(self, time, sending_device, receiving_device, event_description)

    def __str__(self):
        return "ALERT " + Event.__str__(self)


class CancelEvent(Event):
    """Creates an instance of a cancel event."""
    def __init__(self, time: int, sending_device, receiving_device, event_description):
        Event.__init__(self, time, sending_device, receiving_device, event_description)

    def __str__(self):
        return "CANCEL " + Event.__str__(self)


class Device:
    def __init__(self, device_id: int):
        self.id = device_id
        self.propagation_list = []
        self.cancel_list = set()

    def add_propagation(self, device, delay):
        """Takes in a device object, and a certain time delay. Adds prop to the propagation list"""
        self.propagation_list.append((delay, device))

    def is_cancelled(self, text) -> bool:
        """Returns true if text has been cancelled false if not"""
        return text in self.cancel_list

    def cancel(self, text) -> None:
        """Takes in a text and adds it into the objects set"""
        self.cancel_list.add(text)

    def get_propagations(self) -> []:
        return self.propagation_list

    def __str__(self):
        return str(self.id) + ": " + str(self.propagation_list)