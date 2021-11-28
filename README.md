# Okta-Chain-of-Responsibility
## Requirements
- Imagine in your team you have several levels of sales engineers example a new SE, a lead SE, Architect, Staff SE, and the SE Manager. 
- There can be multiple SEs, but only one lead SE or one SE Manager.
- An incoming meeting with the customer must be allocated to the new SE, who is free. If the new SE can’t handle the meeting, he or she must escalate the call to lead SE, if the lead SE is not free or not able to handle it, then the call should be escalated to the SE Manager.

## UML Diagram
![UML-Diagram](https://user-images.githubusercontent.com/20292284/143785587-5074f7f4-fb94-418e-a70e-163f66069388.PNG)


## The Algorithm
1- Initialize the **Requests Queue** and **List of Processors**. Initially **Requests** are in _AVAILABLE_TO_BE_PICKED_ status and **Processors** in _AVAILABLE_ status.  
  
2- As long as there are **Requests**, in the **Requests Queue**, with status _AVAILABLE_TO_BE_PICKED_, keep looping the queue.  
  
3- Check for _AVAILABLE_ **Processor**: check availability first for SE, then Lead SE, and finally for Manager SE.  
  
4- If no **Processor** available, just wait.  
  
5- Once **Processor** assigned for a **Request**, the request's status turns from _AVAILABLE_TO_BE_PICKED_ to _BEING_PROCESSED_, and the processor's status from _AVAILABLE_ to _NOT_AVAILABLE_. The **Processor** processes the **Request** in a **Thread mode**.   
  
6- Once **Request** processed, the **Processor** returns to status **AVAILABLE** and the **Request** is removed from **Requests Queue**.  
  
7- Continue until **Requests Queue** is empty.

## How to execute the code
Just copy and paste the code in a python 3.x editor and execute. No extra modules required.

## How to test the code
To test the code you can play around with the below highlighted values which are the durations, in seconds (for sake of demonstration), to process the meeting requests:  

![test_code](https://user-images.githubusercontent.com/20292284/143786136-4df5ef8c-f83f-4ce8-bfee-7aee2c3efa6a.png)

Check the output of the code to see how requests are being processed.

## Sample outputs:
[sample_output_1.txt](https://github.com/ralphsawaya/Okta-Chain-of-Responsibility/files/7614365/sample_output_1.txt)  

[sample_output_2.txt](https://github.com/ralphsawaya/Okta-Chain-of-Responsibility/files/7614386/sample_output_2.txt)
