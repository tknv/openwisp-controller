from django.db import transaction
from django.db.models.signals import post_delete, post_save

from .base import BaseSubnetDivisionRuleType


class VpnSubnetDivisionRuleType(BaseSubnetDivisionRuleType):
    provision_signal = post_save
    provision_sender = ('config', 'VpnClient')
    provision_dispatch_uid = 'vpn_client_provision_subnet'

    destroyer_signal = post_delete
    destroyer_sender = provision_sender
    destroyer_dispatch_uid = 'vpn_client_destroy_subnet'

    organization_id_path = 'config.device.organization_id'
    subnet_path = 'vpn.subnet'

    @staticmethod
    def post_provision_handler(instance, provisioned, **kwargs):
        def _assign_vpnclient_ip():
            if provisioned['ip_addresses']:
                instance.ip = provisioned['ip_addresses'][0]
                instance.full_clean()
                instance.save()

        if not provisioned:
            return
        transaction.on_commit(_assign_vpnclient_ip)
