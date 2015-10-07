import os
import ra
import pytest
import webtest
import ramses


appdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ramlfile = os.path.join(appdir, 'example.raml')

if not os.path.exists(os.path.join(appdir, 'test.ini')):
    raise Exception("Could not find test.ini in root of project: "
                    "Create a test.ini configured with testing DB and ES index")

testapp = webtest.TestApp('config:test.ini', relative_to=appdir)

# ra entry point: instantiate the API test suite
api = ra.api(ramlfile, testapp)

User = ramses.models.get_existing_model('User')
Story = ramses.models.get_existing_model('Story')
Profile = ramses.models.get_existing_model('Profile')


@api.hooks.before_each
def delete_resources():
    Profile._delete_many(Profile.get_collection())
    Story._delete_many(Story.get_collection())
    User._delete_many(User.get_collection())
    import transaction
    transaction.commit()


@api.hooks.before_each(exclude=['POST /users'])
def create_user():
    User(**api.examples.build('user')).save()
    # XXX: it takes some time for the object to be propagated to ES.
    # This is not ideal at all.
    import time; time.sleep(2)


@api.hooks.before_each(only=['PATCH /users/{username}/profile'])
def create_profile():
    Profile(**api.examples.build('user.profile', user_id='rick')).save()
    import time; time.sleep(2)


@api.hooks.before_each(only=['/stories*'], exclude=['POST'])
def create_story():
    story = Story(**api.examples.build('story', id=1)).save()
    import time; time.sleep(2)

@api.hooks.before_each
def commit():
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
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
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
