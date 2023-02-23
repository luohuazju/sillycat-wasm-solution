import sys
import os
import logging

logging.warn('Logging important warnings')

print('Content-Type: text/plain; charset=UTF-8')
print('Status: 200 OK')
print()

print('Hello from python on', sys.platform)

print()
print('### Arguments ###')
print()

print(sys.argv)

print()
print('### Env Vars ###')
print()

for k, v in sorted(os.environ.items()):
    print(k+':', v)


print()
print('### Files ###')
print()

for f in os.listdir('/wasiconsumer'):
    print(f)
