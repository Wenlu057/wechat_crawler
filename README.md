This project is to build a distributed, stateless, serverless crawler worker.
Usage:
./crawler "subscription account name" <NoSQL host = > <NoSQL Key=>
Crawler will store Htmls, processed pictures into NoSQL, and maintain the name and location table for them.
Crawler should have extensible hookes for reading/writing in datastore, so we can use swith between local storage and NoSQL/MySQL storage conveniently.