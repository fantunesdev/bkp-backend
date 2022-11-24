from backup.databases.database import Device


class DeviceQuery:
    def get_devices(self, session):
        return session.query(Device)
