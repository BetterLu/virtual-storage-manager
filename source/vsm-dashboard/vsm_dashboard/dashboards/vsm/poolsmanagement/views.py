# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Corporation, All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from horizon import exceptions
from horizon import tables
from horizon import forms

from vsm_dashboard.api import vsm as vsmapi
from vsm_dashboard.dashboards.vsm.poolsmanagement import utils
from .form import CreatePool
from .form import CreateErasureCodedPool
from .tables import ListPoolTable

LOG = logging.getLogger(__name__)

class IndexView(tables.DataTableView):
    table_class = ListPoolTable
    template_name = 'vsm/poolsmanagement/index.html'

    def get_data(self):
        pools = []
        try:
            rsp, body = vsmapi.pools_list(self.request, all_pools=True)
            if body:
                pools = body["pool"]
            logging.debug("resp body in view: %s" % pools)
        except:
            exceptions.handle(self.request,
                              _('Unable to retrieve storage pool list. '))
        pools = sorted(pools, lambda x,y: cmp(x['poolId'], y['poolId']))
        #pools = [pool for pool in pools if pool['tag'] != "SYSTEM"]
        return pools

class CreateView(forms.ModalFormView):
    form_class = CreatePool
    template_name = 'vsm/flocking/create.html'
    success_url = reverse_lazy('horizon:vsm:poolsmanagement:index')

class CreateErasureCodedPoolView(forms.ModalFormView):
    form_class = CreateErasureCodedPool
    template_name = 'vsm/flocking/create_ec_pool.html'
    success_url = reverse_lazy('horizon:vsm:poolsmanagement:index')
