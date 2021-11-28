# Okta-Chain-of-Responsibility
## Requirements
- Imagine in your team you have several levels of sales engineers example a new SE, a lead SE, Architect, Staff SE, and the SE Manager. 
- There can be multiple SEs, but only one lead SE or one SE Manager.
- An incoming meeting with the customer must be allocated to the new SE, who is free. If the new SE can’t handle the meeting, he or she must escalate the call to lead SE, if the lead SE is not free or not able to handle it, then the call should be escalated to the SE Manager.

## UML Diagram
![UML-Diagram](https://user-images.githubusercontent.com/20292284/143785587-5074f7f4-fb94-418e-a70e-163f66069388.PNG)


## The Algorithm
1- Initialized list of **Requests** and list of **Processors**  
2- As long as there are **Requests**, in the **Requests Queue**, with status **AVAILABLE_TO_BE_PICKED**, pick that request.  
3- Check for **AVAILABLE** processor: check availability first for SE, then Lead SE, and finally for Manager SE.  
4- If no processor available, just wait.  
5- Once processor selected, the processor starts, **in a thread mode**, processing request and remains in **NOT_AVAILABLE** status for that period of request duration.  
6- Once request processed, the processor returns to status **AVAILABLE** and the Request is removed from queue.  
7- Continue until all **Requests** processed.
