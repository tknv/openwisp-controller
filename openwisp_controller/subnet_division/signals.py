from django.dispatch import Signal

subnet_ips_provisioned = Signal(providing_args=['instance', 'ip_obj'])
