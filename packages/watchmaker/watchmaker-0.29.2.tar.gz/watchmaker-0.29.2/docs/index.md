```{eval-rst}
.. image:: images/cropped-plus3it-logo-cmyk.png
   :width: 140px
   :alt: Powered by Plus3 IT Systems
   :align: right
   :target: https://www.plus3it.com
```
<br>

# watchmaker

Applied Configuration Management

--------------

## Overview

Watchmaker is intended to help provision a system from its initial installation
to its final configuration. It was inspired by a desire to eliminate static
system images with embedded configuration settings (e.g. gold disks) and the
pain associated with maintaining them.

Watchmaker works as a sort of task runner. It consists of "_managers_" and
"_workers_". A _manager_ implements common methods for multiple platforms
(Linux, Windows, etc). A _worker_ exposes functionality to a user that helps
bootstrap and configure the system. _Managers_ are primarily internal
constructs; _workers_ expose configuration artifacts to users. Watchmaker then
uses a common [configuration file](configuration) to determine what
_workers_ to execute on each platform.

## Contents

```{toctree}
:maxdepth: 1

installation.md
configuration.md
usage.md
customization/index.md
troubleshooting/index.md
gotchas/index.md
faq.md
scap.md
findings/index.md
api.md
contributing.md
changelog.md
CentOS-Stream.md
```

## Supported Operating Systems

*   Enterprise Linux 9 (RHEL/Oracle Linux/CentOS Stream/Alma Linux/Rocky Linux)
*   Enterprise Linux 8 (RHEL/Oracle Linux/[CentOS Stream](CentOS-Stream.md))
*   Windows Server 2022
*   Windows Server 2019
*   Windows Server 2016
*   Windows 11
*   Windows 10

## Supported Python Versions

*   Python 3.6 and later

## Supported Salt Versions

*   Salt 2018.3, from 2018.3.4 and later
*   Salt 2019.2, from 2019.2.5 and later
*   Salt 300x, from 3003 and later
