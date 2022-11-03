# COMP90082_2022_SM2_ND_boxjelly

## Project Description 

### Background

This project is developed to enhance practitioners' ability to provide quality Behaviour Support Plans (BSPs) that are consistent with legislation, policy, and good clinical practice, i.e., report requirements of the National Disability Insurance Scheme (NDIS). The proposed methodology is to provide education and supporting resources through the Canvas LMS platform to upskill the relevant workforces and integrate artificial intelligence (AI) to allow the workforce to self-examine through the provision of AI-generated feedback. 

### Problem Domain

The proposed AI agents' training will require enormous data input and the data will be generated through the submission of the practitioners who attended the Canvas LMS module. The raw data as the committed submissions will be in PDF format, hence cannot be used directly for downstream tasks such as AI training. Meanwhile, the information contained in the raw submission should be extracted and organized in efficient formats, so they can be stored and maintained properly within a database. Given the scope of the project, there would be ongoing data input from practitioners through their daily work, therefore, the database should be scalable with the increasing demand.   

### Client Goals

The project team intended to provide feasible solutions to the described problem domain. The following lists the goal of the project:

- implement APIs to receive the submission of the Canvas LMS users efficiently and timely
- extract key information from the raw submission and clean the data before storing them in a structured format in the database
- design a reliable, scalable, and maintainable database 
- provide easily accessible APIs to the base for other downstream tasks

## Github repo

├── docs/                    # Documentation files (Includes requirements, confluence export, release notes)

├── src/                       # src code

├── tests/                    # User/system tests

├── data samples/      # Includes Positive Behaviour Support Plan (PBSP) Document samples
