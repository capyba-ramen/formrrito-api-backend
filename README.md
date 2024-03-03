## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Table Schema](#table-schema)
- [Architecture with Tech Stack](#architecture-with-tech-stack)

## Introduction

This is a form creation platform that enables you to build form, collects responses and wraps up your idea with enriched
user experience

To know more about the details on features, please see [below](#features)

To experience, please visit [here](https://www.formrrito.fun/forms)

## Features

- Create forms or apply template forms. Formulate questions and options
- Upload images for forms and questions
- Utilize AI (by integrating OpenAI api) to enhance question titles/descriptions and recommend question options
  ![gpt](https://github.com/capyba-ramen/formrrito-api-backend/assets/105725219/4b2aabd3-35da-4906-bf8b-6ab1ef5391cf)
  
- Share the form submission page via shortened URL
- Enable form responses from users
- Receive email notifications upon form responses
- View response statistics
  ![image](https://github.com/capyba-ramen/formrrito-api-backend/assets/105725219/9e14ef66-34b3-4c99-95be-251397ed3941)

- Export response data to an Excel sheet
  <img width="1470" alt="excel" src="https://github.com/capyba-ramen/formrrito-api-backend/assets/105725219/45dbf53e-c505-4ca4-a4a9-f5edf4e7e848">


## Table Schema

![image](https://github.com/capyba-ramen/formrrito-api-backend/assets/105725219/9016bfd6-3f49-4ba9-a7e5-8aa6b6fd0329)

## Architecture with Tech Stack

![image](https://github.com/capyba-ramen/formrrito-api-backend/assets/105725219/78406a58-8699-4892-8d83-2e4513272540)

- FastAPI as web framework
- MySQL as database
- Python package alemmbic for database migration
- GitHub Actions for CI/CD
- AWS for deployment and static file storage
- Docker for containerization
- Notion for project management
