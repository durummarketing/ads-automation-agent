#!/usr/bin/env python3
import subprocess
import os

# Set credentials in environment
os.environ['GIT_USERNAME'] = 'durummarketing'
os.environ['GIT_PASSWORD'] = 'ghp_0z0JMYFYwHhxSbECX0pq0BLziPbHYd0AKXPy'

# Configure git to use credential store
subprocess.run(['git', 'config', 'credential.helper', 'store'], cwd='/Users/durummarketing/.openclaw/workspace/durum-ai-agent/ads-automation-agent')

# Try pushing
result = subprocess.run(
    ['git', 'push', '-u', 'https://durummarketing:ghp_0z0JMYFYwHhxSbECX0pq0BLziPbHYd0AKXPy@github.com/durummarketing/ads-automation-agent.git', 'main'],
    cwd='/Users/durummarketing/.openclaw/workspace/durum-ai-agent/ads-automation-agent',
    capture_output=True,
    text=True
)

print(result.stdout)
print(result.stderr)
print(f"Return code: {result.returncode}")
