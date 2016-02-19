import ra
import pytest


# ra entry point: instantiate the API test suite
api = ra.api('example.raml')


@pytest.fixture(scope='session')
def models():
    from nefertari import engine
    return dict(
        User=engine.get_document_cls('User'),
        Profile=engine.get_document_cls('Profile'),
        Story=engine.get_document_cls('Story'))


@pytest.fixture(scope='module', autouse=True)
def drop_storages(request):
    def _drop_es():
        from nefertari.elasticsearch import ES
        ES.delete_index()
    request.addfinalizer(_drop_es)


# perform any necessary test setup
@pytest.fixture(autouse=True)
def setup(req, examples, models):
    User = models['User']
    Story = models['Story']
    Profile = models['Profile']

    import transaction
    import time

    def delete_data():
        Profile._delete_many(Profile.get_collection())
        Story._delete_many(Story.get_collection())
        User._delete_many(User.get_collection())
        transaction.commit()

    def create_user():
        example = examples.build('user')
        user = User(**example).save()
        # XXX: it takes some time for the object to be propagated to ES.
        # This is not ideal at all.
        time.sleep(2)
        return user

    def create_profile(user):
        example = examples.build('user.profile', user=user)
        Profile(**example).save()
        time.sleep(2)

    def create_story():
        example = examples.build('story')
        Story(**example).save()

    delete_data()

    if req.match(exclude='POST /users'):
        user = create_user()

        if req.match('PATCH /users/{username}/profile'):
            create_profile(user)

    if req.match('/stories*', exclude='POST'):
        create_story()

    import transaction
    transaction.commit()


# defining a resource scope:

@api.resource('/users')
def users_resource(users):

    # scope-local pytest fixtures
    #
    # a resource scope acts just like a regular module scope
    # with respect to pytest fixtures:

    @pytest.fixture
    def two_hundred():
        return 200

    # defining tests for methods in this resource:

    @users.get
    def get(req, two_hundred):
        # ``req`` is a callable request object that is pre-bound to the app
        # that was passed into ``ra.api`` as well as the URI derived from
        # the resource (test scope) and method (test) decorators.
        #
        # This example uses the other scope-local fixture defined above.
        response = req()
        assert response.status_code == two_hundred
        assert 'rick' in response

    @users.post
    def post_using_example(req):
        # By default, when JSON data needs to be sent in the request body,
        # Ra will look for an ``example`` property in the RAML definition
        # of the resource method's body and use that.
        #
        # As in WebTest request methods, you can specify the expected
        # status code(s), which will be test the response status.
        response = req(status=201)
        # assert lowercase validator in schema is working:
        assert response.json['email'] == 'rick@example.com'

    # defining a custom user factory; underscored functions are not
    # considered tests (but better to import factories from another module)
    def _user_factory():
        import string
        import random
        name = ''.join(random.choice(string.ascii_lowercase)
                       for _ in range(10))
        email = "{}@example.com".format(name)
        return dict(username=name, email=email, password=name)

    # using the factory:

    @users.post(factory=_user_factory)
    def post_using_factory(req):
        response = req()
        username = req.data['username']
        assert username in response

    # defining a sub-resource:

    @users.resource('/{username}')
    def user_resource(user):

        # this resource will be requested at /users/{username}
        #
        # By default, Ra will look at the ``example`` property for
        # URI parameters as defined in the RAML, and fill the URI
        # template with that. In this case it will use 'rick', which
        # we created in the before-hook.

        @user.get
        def get(req):
            # This is equivalent to the default test for a resource
            # and method:
            req()


@api.resource('/stories')
def stories_resource(stories):

    @stories.resource('/{id}')
    def story_resource(story):

        @story.get
        def get(req):
            response = req()
            assert 'do science' in response

api.autotest()
