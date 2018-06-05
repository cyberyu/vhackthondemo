# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class SampleList(ListResource):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, service_sid, intent_sid):
        """
        Initialize the SampleList

        :param Version version: Version that contains the resource
        :param service_sid: The service_sid
        :param intent_sid: The intent_sid

        :returns: twilio.rest.preview.understand.service.intent.sample.SampleList
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleList
        """
        super(SampleList, self).__init__(version)

        # Path Solution
        self._solution = {'service_sid': service_sid, 'intent_sid': intent_sid}
        self._uri = '/Services/{service_sid}/Intents/{intent_sid}/Samples'.format(**self._solution)

    def stream(self, language=values.unset, limit=None, page_size=None):
        """
        Streams SampleInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode language: The language
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.preview.understand.service.intent.sample.SampleInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(language=language, page_size=limits['page_size'])

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, language=values.unset, limit=None, page_size=None):
        """
        Lists SampleInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode language: The language
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.preview.understand.service.intent.sample.SampleInstance]
        """
        return list(self.stream(language=language, limit=limit, page_size=page_size))

    def page(self, language=values.unset, page_token=values.unset,
             page_number=values.unset, page_size=values.unset):
        """
        Retrieve a single page of SampleInstance records from the API.
        Request is executed immediately

        :param unicode language: The language
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of SampleInstance
        :rtype: twilio.rest.preview.understand.service.intent.sample.SamplePage
        """
        params = values.of({
            'Language': language,
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )

        return SamplePage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of SampleInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of SampleInstance
        :rtype: twilio.rest.preview.understand.service.intent.sample.SamplePage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return SamplePage(self._version, response, self._solution)

    def create(self, language, tagged_text):
        """
        Create a new SampleInstance

        :param unicode language: The language
        :param unicode tagged_text: The tagged_text

        :returns: Newly created SampleInstance
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleInstance
        """
        data = values.of({'Language': language, 'TaggedText': tagged_text})

        payload = self._version.create(
            'POST',
            self._uri,
            data=data,
        )

        return SampleInstance(
            self._version,
            payload,
            service_sid=self._solution['service_sid'],
            intent_sid=self._solution['intent_sid'],
        )

    def get(self, sid):
        """
        Constructs a SampleContext

        :param sid: The sid

        :returns: twilio.rest.preview.understand.service.intent.sample.SampleContext
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleContext
        """
        return SampleContext(
            self._version,
            service_sid=self._solution['service_sid'],
            intent_sid=self._solution['intent_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a SampleContext

        :param sid: The sid

        :returns: twilio.rest.preview.understand.service.intent.sample.SampleContext
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleContext
        """
        return SampleContext(
            self._version,
            service_sid=self._solution['service_sid'],
            intent_sid=self._solution['intent_sid'],
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.Understand.SampleList>'


class SamplePage(Page):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, response, solution):
        """
        Initialize the SamplePage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param service_sid: The service_sid
        :param intent_sid: The intent_sid

        :returns: twilio.rest.preview.understand.service.intent.sample.SamplePage
        :rtype: twilio.rest.preview.understand.service.intent.sample.SamplePage
        """
        super(SamplePage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of SampleInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.preview.understand.service.intent.sample.SampleInstance
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleInstance
        """
        return SampleInstance(
            self._version,
            payload,
            service_sid=self._solution['service_sid'],
            intent_sid=self._solution['intent_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Preview.Understand.SamplePage>'


class SampleContext(InstanceContext):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, service_sid, intent_sid, sid):
        """
        Initialize the SampleContext

        :param Version version: Version that contains the resource
        :param service_sid: The service_sid
        :param intent_sid: The intent_sid
        :param sid: The sid

        :returns: twilio.rest.preview.understand.service.intent.sample.SampleContext
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleContext
        """
        super(SampleContext, self).__init__(version)

        # Path Solution
        self._solution = {'service_sid': service_sid, 'intent_sid': intent_sid, 'sid': sid}
        self._uri = '/Services/{service_sid}/Intents/{intent_sid}/Samples/{sid}'.format(**self._solution)

    def fetch(self):
        """
        Fetch a SampleInstance

        :returns: Fetched SampleInstance
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleInstance
        """
        params = values.of({})

        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )

        return SampleInstance(
            self._version,
            payload,
            service_sid=self._solution['service_sid'],
            intent_sid=self._solution['intent_sid'],
            sid=self._solution['sid'],
        )

    def update(self, language=values.unset, tagged_text=values.unset):
        """
        Update the SampleInstance

        :param unicode language: The language
        :param unicode tagged_text: The tagged_text

        :returns: Updated SampleInstance
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleInstance
        """
        data = values.of({'Language': language, 'TaggedText': tagged_text})

        payload = self._version.update(
            'POST',
            self._uri,
            data=data,
        )

        return SampleInstance(
            self._version,
            payload,
            service_sid=self._solution['service_sid'],
            intent_sid=self._solution['intent_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the SampleInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete('delete', self._uri)

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Preview.Understand.SampleContext {}>'.format(context)


class SampleInstance(InstanceResource):
    """ PLEASE NOTE that this class contains preview products that are subject
    to change. Use them with caution. If you currently do not have developer
    preview access, please contact help@twilio.com. """

    def __init__(self, version, payload, service_sid, intent_sid, sid=None):
        """
        Initialize the SampleInstance

        :returns: twilio.rest.preview.understand.service.intent.sample.SampleInstance
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleInstance
        """
        super(SampleInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'date_created': deserialize.iso8601_datetime(payload['date_created']),
            'date_updated': deserialize.iso8601_datetime(payload['date_updated']),
            'intent_sid': payload['intent_sid'],
            'language': payload['language'],
            'service_sid': payload['service_sid'],
            'sid': payload['sid'],
            'tagged_text': payload['tagged_text'],
            'url': payload['url'],
        }

        # Context
        self._context = None
        self._solution = {
            'service_sid': service_sid,
            'intent_sid': intent_sid,
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: SampleContext for this SampleInstance
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleContext
        """
        if self._context is None:
            self._context = SampleContext(
                self._version,
                service_sid=self._solution['service_sid'],
                intent_sid=self._solution['intent_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The account_sid
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def date_created(self):
        """
        :returns: The date_created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date_updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def intent_sid(self):
        """
        :returns: The intent_sid
        :rtype: unicode
        """
        return self._properties['intent_sid']

    @property
    def language(self):
        """
        :returns: The language
        :rtype: unicode
        """
        return self._properties['language']

    @property
    def service_sid(self):
        """
        :returns: The service_sid
        :rtype: unicode
        """
        return self._properties['service_sid']

    @property
    def sid(self):
        """
        :returns: The sid
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def tagged_text(self):
        """
        :returns: The tagged_text
        :rtype: unicode
        """
        return self._properties['tagged_text']

    @property
    def url(self):
        """
        :returns: The url
        :rtype: unicode
        """
        return self._properties['url']

    def fetch(self):
        """
        Fetch a SampleInstance

        :returns: Fetched SampleInstance
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleInstance
        """
        return self._proxy.fetch()

    def update(self, language=values.unset, tagged_text=values.unset):
        """
        Update the SampleInstance

        :param unicode language: The language
        :param unicode tagged_text: The tagged_text

        :returns: Updated SampleInstance
        :rtype: twilio.rest.preview.understand.service.intent.sample.SampleInstance
        """
        return self._proxy.update(language=language, tagged_text=tagged_text)

    def delete(self):
        """
        Deletes the SampleInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Preview.Understand.SampleInstance {}>'.format(context)
