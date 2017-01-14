# Bare Bones Receiver

This is a simple Google App Engine app that will receive emails and POST them to a Gatsby-based blog (source: https://github.com/calcsam/blog). I hooked up so that it auto-publishes to my website (http://www.mooreshand.com)

I find words come to me more quickly in when I'm composing email, so this is a cheap and easy way to auto publish to my blog without having to deal with email server madness. I also use this as a journal so I can jot some quick notes and send them over.

## How to use

There shouldn't be much setup to this, just change a thing or two and upload:
- Fire up a new GAE app
- Add your secrets in a secrets.py file.
- Deploy!

---

Big thanks to @capitao for prototyping the email receiver I've forked.