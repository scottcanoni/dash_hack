# dash_hack
Python script to capture Amazon Dash button presses and trigger IFTTT maker events

# How to use:
   1. Setup an account in If This Then That (IFTTT): http://www.ifttt.com/
   2. Create a new recipe using the Maker Channel for the IF command:
       a. https://ifttt.com/maker
   3. Update the MAKER_KEY variable below.
   4. Connect your Amazon Dash Button to your network but skip the last step of the setup where they ask you which
      product you want the button to purchase.
   5. Run this program via `python dash-listen.py`.
   6. Push the Amazon Dash Button and take note of its Mac Address.
   7. Overwrite the sample Mac Addresses with your Amazon Dash Button(s) Mac Address(es).
   8. Re-run `python dash-listen.py`.
   9. Now you can configure IFTTT to do anything you want when you push the button.
