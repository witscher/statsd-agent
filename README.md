statsd-agent
============

Statsd client to monitor CPU, Memory, Disk and Network

Installation
============

## Installation (Ubuntu 14.04 LTS)

```
sudo apt-get install python-statsd python-psutil git
# add a system user for statsd-agent
cd /opt/
git clone git@github.com:witscher/statsd-agent.git
sudo adduser --system --group --home /opt/statsd-agent statsd-agent
cd /opt/statsd-agent
cp config.yml.dist config.yml
# if yo want to start statsd-agent automatically:
sudo cp examples/statsd-agent.conf /etc/init/statsd-agent.conf
chown -R statsd-agent:statsd-agent /opt/statsd-agent
```

### Running/Stopping 
Use the Ubuntu service commandwrapper to run/stop statsd-agent:

```
service statsd-agent start
service statsd-agent stop
service statsd-agent restart
service statsd-agent status
```


## Installation (Other Linux/Windows/Mac)
stasd-agent.py is really just a python script. You can run it directly using python command:
```
python statsd-agent.py
```

You can use any daemon tools to make it run as service/background. One of an example is [Supervisor](http://supervisord.org/).


More info about Ubuntu Upstart can be found at http://upstart.ubuntu.com/cookbook/


Configuration
============

## General configuration
The config.yml is mostly self explaining.

## Plugin configuration 

Every plugin can be executed several times, a good example is the disk plugin configuration in the config.yml.example file.
So no matter how many instances of whatsoever you want to monitor, you can do it by just adding the according plugin several times to the configuration

### Plugin Parameters

#### plugin:

the name of the plugin, must match the <plugin>.py file located in plugins/


#### namespace:

Each plugin has its own namespace, so you can change where your statsd metrics belong to.
i.E. if you think the number of nginx Processes doesn not belong to
'hostname.system.processes.nginx' you can change it to 'hostname.nginx.processes.nginx' by simply changing the plugin namespace.


#### more parameters:

each plugin may require and/or accept more parameters. To pre-flight the plugin behaviour, simply execute the plugin with -h itself. i.e. All Parameters with double dashes (--) should work when added to the corresponding plugin in the config file.

so,

```
python plugins/disk.py --mountpoint /home
```

is equal to this configuration:

```
  - plugin:  disk
    namespace: system.disk.home
    mountpoint: /home
```

Plugin developer guidelines
============

* a plugin must have a main function named 'collect()'
* the plugin must work as module and as a exectubale script itself
* a plugin must offer all arguments via argparse wehn called with -h or --help
* the collect() function returns { name : value, name2: value2, ... }  as python  dictionary



License
============

    The MIT License (MIT)
    
    Copyright (c) 2013 Mohd Rozi
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
