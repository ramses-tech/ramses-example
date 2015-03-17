import pyraml.parser

p = pyraml.parser.load('example.raml').resources['/users']

print p

# for attr, value in p.__dict__.iteritems():
    # print attr, value