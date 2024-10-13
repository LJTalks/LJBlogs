![Sign in verify email flow](static/images/signinverify.png)

![Confirm your email address email](static/images/confirm_your_email_address.png)

**Static files **
My project is not currently connecting to some static files, like css and images. It does seem to be connecting to JS scripts in the same directory. Odd. Maybe a links/directory position thing? Shouldn't be whitenoise as I'm testing in gitpod/local. Cloudinary images appear to work... odd.

**Special access to Experimental Features/Beta testing**
Request to Access test and Feedback on Future Features (e.g the Youtube Data Checker)

Must be logged in to request access, and must be accepted for special priviledges.

Add a simple form where users can request access to experimental features. This could be a basic contact form where users submit their interest.

**Working on setting up email functionality**
Have set up email auth for secure login. Need to determine and test edge cases for email confirmations and messages.

**Working on templates** to confirm actions in html and by email (txt and html files). account/base_message.txt and account/base.html could be used for common elements.

e.g. base_message.txt

```
{% block body %}{% endblock %}

--
LJ Talks
{% block footer %}
If you no longer wish to receive these emails, you can unsubscribe here: {{ unsubscribe_url }}
{% endblock %}
```

e.g. email_confirmation_message.txt:

```
{% extends "base_message.txt" %}

{% block body %}
Hello {{ user.username }},

Please click the link below to confirm your email:

{{ activate_url }}
{% endblock %}
```

Need to **ensure contact details and unsubscribe options** happen in each instance.

Have set up emails to potentially keep my email list database within this project.

**Can send and receive emails** from within this project but that can be explanded to be more intuitive and user friedly, with a **front end** for admin.

Likely need to **add a "User profile"** type app for recording user actions, interactions, messages set, products purchased, posts liked, comments etc. It could become a bit of a monster!

**Next Steps** for Automating Email Subscribe/Unsubscribe:
Automate the management of the email list and unsubscribed users by storing subscription statuses in the database and building an admin interface to manage email subscriptions.

Looks likely that a **profile app (user perspective)** would be relevant, and also an** email management app (admin perspective)**...

**Unsubscribe** view is currently in **blog app**. This should be moved and separated when the profile or emailmanagement app exists.

### Add email authentication

I think I've almost done this!

But we need to make this prettier

![EMail verification checker](static/images/email_verification.png)

### Add a welcome email

<!-- This is TBA in templates/welcome_email.html -->

It's only right to offer an Opt-Out of receiving "list" emails _Without Losing Energy_:

I want to maintain the excitement even when providing users with an easy opt-out option. Something like this:

```
<p>We’re excited to have you on board, but if for any reason you’d prefer to stop receiving emails, you can <a href="unsubscribe-link">unsubscribe here</a>. Don’t worry, you can always rejoin later!</p>
```

### Update my new 404 page.

No one likes a broken link.

I added a page to catch 404 errors. If the user should encounter this issue I would like to provide some assistance to stay on my site.

I have resisted the urge to create a page full of cute kittens to soothe the user, and instead have useful page that will help them move on without too much additional distress.

The **404, not found error page** will offer a reassuring, on brand page offering options to **message me directly** about what they were hoping to find, and also **options** to redirect somewhere useful (like the homepage).

If the user was already on my site, they can **easily** get back to the page they were previously on, or the **homepage**.

The message fits with the website's general structure and design, to minimise any sufffering to the user, and encourage them to give the site another chance.

Future plans - Use JavaScript to Check the Referrer: Add a button that will either take the user back to the previous page if they came from somewhere on the site or to the homepage if there is no referrer.
