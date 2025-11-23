import enum


class MusicPlatform(str, enum.Enum):
    SPOTIFY = "spotify"
    YANDEX = "yandex"
    APPLE = "apple"
    VK = "vk"
    OTHER = "other"
