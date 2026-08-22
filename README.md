# Actuarial Data Analytics Platform

## Overview

This project is an end-to-end actuarial data analytics platform designed for pension fund valuation, population projection, trend analysis, and risk modelling.

The platform combines actuarial modelling with modern data engineering and software engineering, including Python, SQL Server, FastAPI, Docker, data ingestion, automated calculations, and database integration.

The API receives actuarial input data and assumptions, ingests and stores the data in SQL Server, retrieves the required data for actuarial processing, runs actuarial calculations and projections using Python, stores the calculated results back in SQL Server, and returns the results through the API.

The entire application is containerized using Docker, creating a reproducible environment for the complete  data pipeline.

The Dockerized application includes:

- FastAPI application
- Data ingestion
- Data cleaning and transformation
- SQL Server integration
- Actuarial calculation modules
- Pension liability calculations
- Normal cost calculations
- Salary projections
- Survival probability calculations
- Retirement projections
- Survivor projections
- Population projections
- Sensitivity analysis
- Result generation
- Result storage in SQL Server
- API-based result retrieval

---

# End-to-End Pipeline

The main purpose of the platform is to automate the complete data workflow.

```text
                         API Request
                              |
                              v
                    FastAPI Application
                              |
                              v
                       Data Ingestion
                              |
                              v
                     SQL Server Database
                              |
                  +-----------+-----------+
                  |                       |
                  v                       v
            Employee Data           Assumptions
            Retired Data            Life Tables
            Survivor Data
                  |                       |
                  +-----------+-----------+
                              |
                              v
                    Actuarial Processing
                              |
                              v
                  Pension Projection Engine
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
         Liability        Population       Sensitivity
         Projection       Projection        Analysis
             |                |                |
             +----------------+----------------+
                              |
                              v
                    Calculation Results
                              |
                              v
                     SQL Server Database
                              |
                              v
                         FastAPI
                              |
                              v
                       JSON Response

# Future Development

The next stage of the project will focus on transforming the current actuarial platform into a more scalable, production-oriented analytics solution.

## AWS Cloud Deployment

The platform will be deployed to Amazon Web Services (AWS), allowing the containerized actuarial API and database environment to operate in a scalable cloud infrastructure.

Planned technologies and services include:

- Amazon ECS / AWS Fargate
- Amazon RDS
- Amazon S3
- AWS networking and security
- Cloud-based API deployment

The objective is to move the current Docker-based local platform toward a production-style cloud environment.

## Power BI Business Intelligence

A Power BI dashboard will be developed to provide an interactive business intelligence layer on top of the actuarial results stored in the database.

The dashboard will provide visual analysis of:

- Pension liabilities
- Normal cost
- Employee population
- Retired population
- Survivor population
- Population projections
- Salary trends
- Age distribution
- Sensitivity analysis
- Key actuarial indicators

The goal is to transform actuarial calculations into clear and interactive insights that support actuarial analysis and management decision-making.

## Automated Testing

Automated testing will be introduced to improve the reliability and maintainability of the platform.

Future testing will cover:

- Actuarial calculation functions
- Data validation
- API endpoints
- Database operations
- Projection models
- Edge cases and invalid inputs

## CI/CD Automation

A continuous integration and deployment workflow will be implemented using GitHub Actions.

The planned workflow will automatically:

1. Run automated tests
2. Validate the application
3. Build Docker images
4. Push images to a container registry
5. Deploy updated versions to AWS


