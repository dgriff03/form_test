# Test form application


This form allows someone to create an application which immediate steps into a timed form flow. The form will auto-adance after 3 minutes at each stage.


Things that still need to be added:
- Data validation
- Swapping print statments (used for debuging) for actual logging
- Admin / list views to look at collected results
- Database setup for questions flows rather than 1 hard coded list
- Some sense of security (form auth token for cross-site request forgery protection, obfuscate form ids)
- Client side validation on sign-up flow.
- Prevent the same exam from being taken twice...


Note, original app cloned from:
https://github.com/yefim/flask-heroku-sample