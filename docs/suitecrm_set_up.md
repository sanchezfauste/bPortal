# SuiteCRM set up

## Enable AOP Account Creation
In order to be able to create new accounts in the portal, you have to edit the AOP settings of SuiteCRM. To do that, go to administration pannel of SutieCRM and edit the `AOP Settings`.

`Enable AOP` and `Enable External Portal` must be checked.

Finally specify the portal URL on `Joomla URL` field. For example, `https://portal.example.com`.

Now you can create new accounts going to `Contacts` module, selecting a contact and clicking on `Create Portal User` user.

## Needed PR
The folliwing PRs are needed to make bPortal work properly:  
[PR 5755](https://github.com/salesagility/SuiteCRM/pull/5755)  
[PR 5745](https://github.com/salesagility/SuiteCRM/pull/5745)
