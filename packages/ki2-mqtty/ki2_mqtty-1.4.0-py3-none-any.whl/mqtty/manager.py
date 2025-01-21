from __future__ import annotations
from typing import TYPE_CHECKING, overload
from typing_extensions import Optional, Self, Literal, TypeAlias, Callable
import threading
import asyncio
import time


if TYPE_CHECKING:
    from .mqtty import MqttyDevice
    from .types import MqttCallback
    from ki2_python_utils import Json


OnRegisterCallback: TypeAlias = Callable[[str], None]
OnSerialErrorCallback: TypeAlias = Callable[["MqttyDevice", Exception], None]


class MqttyDevicesManager:
    __devices: dict[str, MqttyDevice]

    on_mqtt_message: Optional[MqttCallback]
    on_register: Optional[OnRegisterCallback]
    on_serial_error: Optional[OnSerialErrorCallback]

    __defered_unregister: list[str]

    def __init__(self) -> None:
        self.__devices = {}
        self.on_mqtt_message = None
        self.on_register = None
        self.on_serial_error = None
        self.__defered_unregister = []

    @property
    def topics(self) -> list[str]:
        return list(self.__devices.keys())

    def has_topic(self, topic: str) -> bool:
        return topic in self.__devices.keys()

    @property
    def devices(self) -> list[MqttyDevice]:
        return list(self.__devices.values())

    def set_callback(self, cb: MqttCallback, /) -> Self:
        self.on_mqtt_message = cb
        return self

    def register(self, topic: str, device: MqttyDevice) -> Self:
        if topic in self.__devices.keys():
            raise ValueError(f"Device with topic {topic} already registered")
        device.on_mqtt_message = self._handle_message
        self.__devices[topic] = device

        if self.on_register is not None:
            self.on_register(topic)

        return self

    def unregister(self, topic: str, defered: bool = False) -> Self:
        if topic not in self.__devices.keys():
            raise ValueError(f"No device with topic '{topic}' registered")
        if defered:
            self.__defered_unregister.append(topic)
        else:
            del self.__devices[topic]
        return self

    def _handle_defered_unregister(self) -> None:
        for topic in self.__defered_unregister:
            del self.__devices[topic]
        self.__defered_unregister = []

    def _get_device_topic(self, device: MqttyDevice) -> str | None:
        for topic, device_item in self.__devices.items():
            if device_item == device:
                return topic
        return None

    def _handle_message(self, topic: str, payload: str) -> None:
        if self.on_mqtt_message is not None:
            self.on_mqtt_message(topic, payload)

    def tick_read(self) -> None:
        for device in self.__devices.values():
            try:
                device.tick_read()
            except Exception as e:
                topic = self._get_device_topic(device)
                if topic is not None:
                    self.unregister(topic, defered=True)
                if self.on_serial_error is not None:
                    self.on_serial_error(device, e)
                else:
                    raise e
        self._handle_defered_unregister()

    def send(self, topic: str, message: str | Json) -> Self:
        if topic not in self.__devices.keys():
            raise ValueError(f"No device with topic '{topic}' registered")

        try:
            self.__devices[topic].send(message)
        except Exception as e:
            self.unregister(topic)
            if self.on_serial_error is not None:
                self.on_serial_error(self.__devices[topic], e)
            else:
                raise e
        return self

    def reset_input_buffers(self) -> Self:
        for device in self.__devices.values():
            device.reset_input_buffer()
        return self


class ThreadedMqttyDevicesManager(MqttyDevicesManager):
    __thread: threading.Thread

    __started: bool = False

    def __init__(self):
        super().__init__()
        self.__thread = threading.Thread(target=self._run)
        self.__thread.daemon = True

    def _run(self) -> None:
        self.reset_input_buffers()
        while self.__started:
            self.tick_read()
            time.sleep(0.1)

    def start(self) -> Self:
        self.__started = True
        self.__thread.start()
        return self

    def stop(self) -> Self:
        self.__started = False
        self.__thread.join()
        return self

    def wait_forever(self) -> None:
        if self.__thread.is_alive():
            self.__thread.join()

    def run_forever(self) -> None:
        if not self.__thread.is_alive():
            self.start()
        self.wait_forever()


class AsyncMqttyDevicesManager(MqttyDevicesManager):
    __started: bool = False

    async def loop(self) -> None:
        self.__started = True
        self.reset_input_buffers()
        while self.__started:
            self.tick_read()
            await asyncio.sleep(0.1)

    def stop(self) -> Self:
        self.__started = False
        return self


__manager__: MqttyDevicesManager | None = None


@overload
def manager_setup(mode: Literal["threaded"]) -> ThreadedMqttyDevicesManager: ...


@overload
def manager_setup(mode: Literal["async"]) -> AsyncMqttyDevicesManager: ...


@overload
def manager_setup(
    mode: Literal["threaded"] | Literal["async"],
) -> ThreadedMqttyDevicesManager | AsyncMqttyDevicesManager: ...


def manager_setup(
    mode: Literal["threaded"] | Literal["async"],
) -> ThreadedMqttyDevicesManager | AsyncMqttyDevicesManager:
    global __manager__

    if __manager__ is not None:
        raise Exception("Manager already setup")

    if mode == "threaded":
        __manager__ = ThreadedMqttyDevicesManager()
    elif mode == "async":
        __manager__ = AsyncMqttyDevicesManager()
    else:
        raise Exception("Invalid mode")

    return __manager__


def get_manager() -> MqttyDevicesManager:
    global __manager__
    if __manager__ is None:
        raise Exception("Manager not setup")
    return __manager__
