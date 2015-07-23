from ra import Tester
from pyramid.paster import bootstrap


def main():
    application = bootstrap('local.ini')['app']
    Tester(application, 'example.raml').run()

main()
