# com.castsoftware.uc.springwebflow

# Spring Web Flow Analyzer

# Introduction : 

Spring Web Flow (SWF) is the sub-project of the Spring Framework that focuses on providing the infrastructure for building and running rich web applications. The project tries to solve 3 core problems facing web application developers:
* How do you express page navigation rules?
* How do you manage navigation and conversational state?
* How do you facilitate modularization and reuse?

In Spring Web Flow, a web flow answers all of the above questions: it captures navigational rules allowing the Spring Web Flow execution engine to manage a conversation and the associated state. At the same time, a web flow is a reusable web application module.

This technical package is deliver "as-is". It has been used in a limited number of situations.
This package has been tested in CAST 8.1.x 

## Additional types of objects bring by this extension 
Objects being part of Spring WebFlow Metamodel : View-State, Action-State, Decision-State, Subflow, On-Start, ... 

![Spring WebFlow](/springWebFlowMetamodel.jpg)

## Cases covered by this extension 

The following cases are covered by the extension : 
- creation of objects for Spring Web Flow artefacts 
- links between Spring Web Flow objects 
- links from view-state to view and model 
- links between Spring Web Flow objects and Java classes & methods 
- ... 

## Sample transactions Spring Web Flow end to end graphical view 
to be done 

## TCC configuration
All the "Evaluate" (defined in the metamodel) have to be defined as entry points instead of the eFile. 

# TODO 
Analysis Unit (or webapp) to be taken into account for determination of the beans (to be able to delete duplicates) 
Analysis Unit (or webapp) to be taken into account for determination of the jsp and tiles (to be able to delete duplicates) 
Manage inheritance between Web Flow definition in different files 
To be described more 

# How to contribute
For bugs, feature requests, and contributions contact Thierry Guégan t.guegan@castsoftware.com.
You may also send a thank you if you find this useful.
