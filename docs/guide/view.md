# Class Based Views

REST channels provide `SocketView` class.

It's a wrapping around functional views like in django and have method `send`,
that send data to channel or group as `text` or `binary`.

    def send(self, channel_or_group, data, content_type='text', close=False):
        ...

For example:
`routing.py`

    routing = [
        ...
        route(
            'websocket.receive',
            CompositionSocketView.as_view(),
            path=r'/(?P<composition_id>\d+)/$'
        ),
        ...
    ]
    
`views.py`

    class CompositionSocketView(SocketView):
        COMPOSITION_GROUP_TEMPLATE = 'Composition-%s'
        
        # wrap django-channels decorators to `rest_channels` decorator 
        @rest_channels(channel_session)
        def receive(self, request, *args, **kwargs):
            # Get composition id from path 
            composition_id = kwargs.get('composition_id')
            # Get data from request as usual.
            method = request.data.get('method')
            # This `data` from incoming json.
            data = request.data.get('data')
            # Do something useful
            user = self.check_composition_perms(data, composition_id)
            # Pass user.id to channel_session
            request.channel_session['user'] = user.id
            # Add user to group
            Group(self.COMPOSITION_GROUP_TEMPLATE % composition_id).add(request.reply_channel)
            self.send(
                request.reply_channel,
                CompositionVersionSerializer(
                    {
                        'method': 'sign_in',
                        'user': user.id,
                        'data': composition.versions.last(),
                        'status': status.HTTP_200_OK,
                    }
                ).data
            )
        
`serializers.py`

    class SocketResponseSerializer(serializers.Serializer):
        status = serializers.IntegerField(min_value=100, max_value=600)
        method = serializers.CharField()
        user = serializers.IntegerField()
    
    
    class SocketCompositionVersionSerializer(SocketResponseSerializer):
        data = CompositionVersionSerializer(required_fields=('tracks',))