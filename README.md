Evernote font adjuster
=============
Evernote ipad client doesn't allow to adjust font size. However all notes are in some kind of HTML, so there is a way to do it from backdoor way.

Configuration
-------
### Project local configuration
```
python3 bootstrap-buildout.py (add flag --allow-site-packages for windows machine)
bin/buildout
```

### Buildout Windows installation issues
To properly compile depended C libraries (during bildout run) the following changes in environment are required:

```
SET VS90COMNTOOLS=%VS100COMNTOOLS%  # with Visual Studio 2010 installed (Visual Studio Version 10)
```
or
```
SET VS90COMNTOOLS=%VS110COMNTOOLS%  # with Visual Studio 2012 installed (Visual Studio Version 11)
```
or

```
SET VS90COMNTOOLS=%VS120COMNTOOLS%  # with Visual Studio 2013 installed (Visual Studio Version 12)
```
The list of precompiled libraries for windows you can find here http://www.lfd.uci.edu/~gohlke/pythonlibs/

### Configuration example
To make this piece source code to work properly, you have to provide configuration file 
in environment variable 

```
EFA_CONFIG=/path/to/conf.yaml
```

Exapmle:
```yaml
logging:
  level: 10 #10 is for Debug logs, 30 is for Warning by Default
 
evernote:
  auth_token: "blah-blah-blah" #Evernote Auth token
  sandbox: True #Use https://sandbox.evernote.com/ instead of prod
  notebooks: # List of Notebooks names to adjust
    - "notebook1"
    - "notebook2"

font_size: 20 #Font size you are going to make your notes
line_height: 150 #Line height interval
```
