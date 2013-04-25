#coding: utf-8

import socket

from django.db import models
from django.core.management import BaseCommand
from optparse import make_option


class Command(BaseCommand):
    args = ''
    help = 'Sample implementation of Gopher protocol just for fun.'

    option_list = BaseCommand.option_list + ()

    def dump_model_record(self, record):
        return u'\r\n\r\n'.join([u'%s:\r\n%s' %
                                (f.verbose_name or f.attname, unicode(getattr(record, f.attname)))
                                for f in record._meta.fields])

    def handle(self, *args, **options):
        model_mapping = {}

        for model_cls in models.get_models():
            if isinstance(model_cls._meta.verbose_name, basestring):
                model_mapping[model_cls.__name__] = model_cls

        local_hostname = '0.0.0.0'
        bind_port = 70

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((local_hostname, bind_port))

        print u'Listening for connections on %s:%i...' % (local_hostname, bind_port)

        sock.listen(5)

        while True:
            (clientsock, address) = sock.accept()

            print 'Accepted connection from %s:%i!' % address
            chunk = clientsock.recv(255)
            chunk = chunk.strip()

            print 'Received reference: %s' % chunk
            if chunk == '/' or not chunk:
                reply = '1' + u'\n1'.join(
                        u'\t'.join((m._meta.verbose_name, '/%s' % m.__name__, '127.0.0.1', '70'))
                        for m in sorted(model_mapping.values(), key=lambda x: x._meta.verbose_name))
            else:
                parts = chunk[1:].split('/')
                if len(parts) == 1:
                    model = model_mapping[parts[0]]
                    count = model.objects.count()

                    info = u'iModel: "%s" Number of records: %i\tfake\t(NULL)\t0\r\n0' % (model._meta.verbose_name, count)

                    reply = info + u'\n0'.join(u'\t'.join((unicode(rec), '/%s/%i' % (parts[0], rec.id), local_hostname, unicode(bind_port))) for rec in model.objects.all())
                else:
                    model = model_mapping[parts[0]]
                    rec_id = int(parts[1])

                    rec = model.objects.get(id=rec_id)
                    reply = self.dump_model_record(rec)

            reply += '\r\n.\r\n'
            print 'Sending reply (%s symbols)...' % len(reply)
            clientsock.sendall(reply.encode('utf-8'))

            print 'Closing connection.\r\n'
            clientsock.close()
