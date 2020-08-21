# webclipboard

#### Share your clipboard with your friends using the web

This script facilitates automating transfer of clipboard from one or more users to their friend using https://dweet.io

##### Installation
`pip install -U webclipboard`


##### Sharing your clipboard
`webclipboard --mode=master --channel=math123 --debug`

##### Receiving somen's clipboard
`webclipboard --mode=slave --channel=math123 --debug`

** Make sure both master and slaves use the same channel name**
