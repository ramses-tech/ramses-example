from ra import RAMLTester
from pyramid.paster import bootstrap


def main():
    application = bootstrap('local.ini')['app']
    RAMLTester(application, 'example.raml').test()

main()
