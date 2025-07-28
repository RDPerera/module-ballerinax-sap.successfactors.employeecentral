from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any, List
import uuid
import random
from datetime import datetime, timedelta

app = FastAPI()

# Comprehensive mock data for all SAP SuccessFactors Employee Central entities
MOCK_DATA: Dict[str, List[Dict[str, Any]]] = {
    # Employment Information
    "EmpEmployment": [
        {"personIdExternal": "john123", "userId": "EMP001", "startDate": "2020-01-01", "employmentStatus": "Active"},
        {"personIdExternal": "jane456", "userId": "EMP002", "startDate": "2019-06-15", "employmentStatus": "Active"}
    ],
    "EmpJob": [
        {"seqNumber": 1, "startDate": "2020-01-01", "userId": "EMP001", "jobTitle": "Engineer"},
        {"seqNumber": 2, "startDate": "2019-06-15", "userId": "EMP002", "jobTitle": "Manager"}
    ],
    "EmpBeneficiary": [
        {"beneficiaryId": "BEN001", "userId": "EMP001", "firstName": "John", "lastName": "Doe"}
    ],
    "EmpEmploymentTermination": [
        {"userId": "EMP003", "terminationDate": "2023-12-31", "reason": "Resignation"}
    ],
    "EmpPensionPayout": [
        {"userId": "EMP001", "payoutAmount": 50000, "payoutDate": "2023-01-01"}
    ],
    "EmpWorkPermit": [
        {"userId": "EMP001", "permitType": "H1B", "expirationDate": "2025-12-31"}
    ],
    "EmpJobRelationships": [
        {"userId": "EMP001", "relatedUserId": "EMP002", "relationshipType": "Reports To"}
    ],
    "PersonEmpTerminationInfo": [
        {"userId": "EMP003", "lastWorkingDay": "2023-12-31", "finalPayDate": "2024-01-15"}
    ],
    "HireDateChange": [
        {"code": "HDC001", "newHireDate": "2021-05-01", "userId": "EMP001"}
    ],

    # Alternative Cost Distribution
    "EmpCostDistribution": [
        {"effectiveStartDate": "2023-01-01", "usersSysId": "EMP001", "percentage": 100}
    ],
    "EmpCostDistributionItem": [
        {"EmpCostDistribution_effectiveStartDate": "2023-01-01", "EmpCostDistribution_usersSysId": "EMP001", "externalCode": 1, "costCenter": "CC001"}
    ],

    # Employee Profile - Background entities
    "Background_Community": [
        {"backgroundElementId": 1, "userId": "EMP001", "organization": "Community Center", "role": "Volunteer"}
    ],
    "Background_Courses": [
        {"backgroundElementId": 1, "userId": "EMP001", "courseName": "Project Management", "completionDate": "2022-06-01"}
    ],
    "Background_Benefitselection": [
        {"backgroundElementId": 1, "userId": "EMP001", "benefitType": "Health Insurance", "coverage": "Family"}
    ],
    "Background_OutsideWorkExperience": [
        {"backgroundElementId": 1, "userId": "EMP001", "company": "Previous Corp", "position": "Developer", "startDate": "2018-01-01", "endDate": "2019-12-31"}
    ],
    "Background_Promotability": [
        {"backgroundElementId": 1, "userId": "EMP001", "promotabilityRating": "High", "assessmentDate": "2023-01-01"}
    ],
    "Background_Fsaelection": [
        {"backgroundElementId": 1, "userId": "EMP001", "fsaType": "Healthcare", "electionAmount": 2500}
    ],
    "Background_Compensation": [
        {"backgroundElementId": 1, "userId": "EMP001", "salary": 75000, "effectiveDate": "2023-01-01"}
    ],
    "Background_Memberships": [
        {"backgroundElementId": 1, "userId": "EMP001", "organization": "Professional Association", "membershipType": "Active"}
    ],
    "Background_Documents": [
        {"backgroundElementId": 1, "userId": "EMP001", "documentType": "Certificate", "documentName": "AWS Certification"}
    ],
    "Background_FuncExperience": [
        {"backgroundElementId": 1, "userId": "EMP001", "function": "Software Development", "years": 5}
    ],
    "Background_TalentPool": [
        {"backgroundElementId": 1, "userId": "EMP001", "talentPool": "High Potential", "dateAdded": "2023-01-01"}
    ],
    "Background_Googledocs": [
        {"backgroundElementId": 1, "userId": "EMP001", "documentUrl": "https://docs.google.com/document/123", "title": "Resume"}
    ],
    "Background_Awards": [
        {"backgroundElementId": 1, "userId": "EMP001", "awardName": "Employee of the Month", "awardDate": "2023-03-01"}
    ],
    "Background_Education": [
        {"backgroundElementId": 1, "userId": "EMP001", "school": "University of Technology", "degree": "Computer Science", "graduationDate": "2018-05-01"}
    ],
    "Background_Mobility": [
        {"backgroundElementId": 1, "userId": "EMP001", "willingToRelocate": True, "preferredLocations": "New York, San Francisco"}
    ],
    "Background_VarPayEmpHistData": [
        {"backgroundElementId": 1, "userId": "EMP001", "bonus": 10000, "year": 2023}
    ],
    "Background_InsideWorkExperience": [
        {"backgroundElementId": 1, "userId": "EMP001", "department": "Engineering", "position": "Senior Developer", "startDate": "2020-01-01"}
    ],
    "Background_PreferredNextMove": [
        {"backgroundElementId": 1, "userId": "EMP001", "preferredRole": "Team Lead", "timeframe": "1-2 years"}
    ],
    "UserBadges": [
        {"badgeId": "BADGE001", "userId": "EMP001", "badgeName": "Innovation Award", "earnedDate": "2023-06-01"}
    ],
    "BadgeTemplates": [
        {"templateId": "TEMPLATE001", "badgeName": "Excellence Award", "description": "For outstanding performance"}
    ],
    "EPPublicProfile": [
        {"userId": "EMP001", "publicProfile": True, "profileSummary": "Experienced software engineer"}
    ],

    # Skills Management
    "CertificationContent": [
        {"certificationId": "CERT001", "certificationName": "AWS Solutions Architect", "issuer": "Amazon"}
    ],
    "FamilyEntity": [
        {"familyId": "FAM001", "familyName": "Software Engineering", "description": "Software development roles"}
    ],
    "CertificationEntity": [
        {"certificationId": "CERT001", "certificationName": "PMP", "validityPeriod": 36}
    ],
    "JobResponsibilityContent": [
        {"responsibilityId": "RESP001", "description": "Lead development projects", "category": "Leadership"}
    ],
    "InterviewQuestionContent": [
        {"questionId": "Q001", "question": "Describe your experience with cloud technologies", "category": "Technical"}
    ],
    "JobResponsibilityEntity": [
        {"responsibilityId": "RESP001", "responsibility": "Project Management", "competencyLevel": "Expert"}
    ],
    "RatedSkillMapping": [
        {"mappingId": "MAP001", "skillId": "SKILL001", "proficiencyLevel": "Advanced"}
    ],
    "RoleCompetencyBehaviorMappingEntity": [
        {"mappingId": "RCBM001", "roleId": "ROLE001", "competencyId": "COMP001", "behaviorId": "BEH001"}
    ],
    "RoleEntity": [
        {"roleId": "ROLE001", "roleName": "Software Engineer", "department": "Engineering"}
    ],
    "JobProfileLocalizedData": [
        {"profileId": "JP001", "locale": "en_US", "title": "Senior Developer", "description": "Lead software development"}
    ],
    "JobCodeMappingEntity": [
        {"mappingId": "JCM001", "jobCode": "ENG001", "profileId": "JP001"}
    ],
    "CompetencyType": [
        {"typeId": "CT001", "typeName": "Technical", "description": "Technical competencies"}
    ],
    "EmploymentConditionContent": [
        {"conditionId": "EC001", "condition": "Full-time", "description": "Regular full-time employment"}
    ],
    "FamilyCompetencyMappingEntity": [
        {"mappingId": "FCM001", "familyId": "FAM001", "competencyId": "COMP001"}
    ],
    "PhysicalReqEntity": [
        {"reqId": "PR001", "requirement": "Standing", "description": "Ability to stand for extended periods"}
    ],
    "InterviewQuestionEntity": [
        {"questionId": "IQ001", "question": "Technical problem solving", "difficulty": "Medium"}
    ],
    "BehaviorMappingEntity": [
        {"mappingId": "BM001", "behaviorId": "BEH001", "competencyId": "COMP001"}
    ],
    "SkillEntity": [
        {"skillId": "SKILL001", "skillName": "Java Programming", "category": "Programming Languages"}
    ],
    "PhysicalReqContent": [
        {"reqId": "PRC001", "requirement": "Lifting", "weight": "25 lbs"}
    ],
    "SkillContent": [
        {"skillId": "SC001", "skillName": "Python", "proficiencyLevels": ["Beginner", "Intermediate", "Advanced"]}
    ],
    "RoleCompetencyMappingEntity": [
        {"mappingId": "RCM001", "roleId": "ROLE001", "competencyId": "COMP001", "requiredLevel": "Proficient"}
    ],
    "SelfReportSkillMapping": [
        {"mappingId": "SRS001", "userId": "EMP001", "skillId": "SKILL001", "selfRating": "Expert"}
    ],
    "JobProfile": [
        {"profileId": "JP001", "jobTitle": "Senior Software Engineer", "department": "Engineering", "level": "Senior"}
    ],
    "FamilySkillMappingEntity": [
        {"mappingId": "FSM001", "familyId": "FAM001", "skillId": "SKILL001"}
    ],
    "RoleSkillMappingEntity": [
        {"mappingId": "RSM001", "roleId": "ROLE001", "skillId": "SKILL001", "proficiencyRequired": "Advanced"}
    ],
    "JobDescTemplate": [
        {"templateId": "JDT001", "templateName": "Software Engineer Template", "content": "Job description template"}
    ],
    "SkillProfile": [
        {"profileId": "SP001", "userId": "EMP001", "skillAssessmentDate": "2023-01-01"}
    ],
    "CompetencyEntity": [
        {"competencyId": "COMP001", "competencyName": "Problem Solving", "definition": "Ability to solve complex problems"}
    ],
    "CompetencyContent": [
        {"contentId": "CC001", "competencyId": "COMP001", "behaviorExample": "Analyzes complex situations"}
    ],
    "RelevantIndustryEntity": [
        {"industryId": "IND001", "industryName": "Technology", "sector": "Software"}
    ],
    "RoleTalentPoolMappingEntity": [
        {"mappingId": "RTPM001", "roleId": "ROLE001", "talentPoolId": "TP001"}
    ],
    "EmploymentConditionEntity": [
        {"conditionId": "ECE001", "conditionName": "Remote Work", "allowsRemote": True}
    ],
    "JobDescSection": [
        {"sectionId": "JDS001", "sectionName": "Responsibilities", "content": "Key job responsibilities"}
    ],
    "RelevantIndustryContent": [
        {"contentId": "RIC001", "industryId": "IND001", "experience": "3 years minimum"}
    ],
    "PositionEntity": [
        {"positionId": "POS001", "positionTitle": "Senior Developer", "department": "Engineering"}
    ],
    "PositionCompetencyMappingEntity": [
        {"mappingId": "PCM001", "positionId": "POS001", "competencyId": "COMP001"}
    ],
    "PositionSkillMappingEntity": [
        {"mappingId": "PSM001", "positionId": "POS001", "skillId": "SKILL001"}
    ],
    "JDTemplateFamilyMapping": [
        {"mappingId": "JTFM001", "templateId": "JDT001", "familyId": "FAM001"}
    ],

    # Payroll & Timesheets
    "EmployeeTimeSheet": [
        {"externalCode": "TS001", "userId": "EMP001", "weekEnding": "2023-12-08", "totalHours": 40}
    ],
    "ExternalAllowance": [
        {"externalCode": "ALLOW001", "userId": "EMP001", "allowanceType": "Meal", "amount": 500}
    ],
    "TimeCollector": [
        {"externalCode": "TC001", "collectorName": "Regular Time", "description": "Standard working hours"}
    ],
    "ExternalTimeRecord": [
        {"externalCode": "TR001", "userId": "EMP001", "date": "2023-12-01", "hours": 8}
    ],
    "ExternalTimeData": [
        {"externalCode": "TD001", "userId": "EMP001", "timeType": "Regular", "hours": 8}
    ],
    "DataReplicationProxy": [
        {"externalCode": "DRP001", "entityType": "TimeData", "status": "Processed"}
    ],
    "EmployeeTimeSheetEntry": [
        {"entryId": "TSE001", "timeSheetCode": "TS001", "date": "2023-12-01", "hours": 8}
    ],
    "EmployeeTimeValuationResult": [
        {"resultId": "TVR001", "userId": "EMP001", "valuationAmount": 640}
    ],
    "AllowanceRecording": [
        {"recordingId": "AR001", "allowanceCode": "ALLOW001", "recordedDate": "2023-12-01"}
    ],
    "AvailableAllowanceType": [
        {"typeId": "AAT001", "allowanceType": "Transportation", "maxAmount": 200}
    ],
    "ExternalTimeSegment": [
        {"segmentId": "ETS001", "timeRecordCode": "TR001", "startTime": "09:00", "endTime": "17:00"}
    ],
    "TimeRecording": [
        {"recordingId": "TR001", "userId": "EMP001", "recordingDate": "2023-12-01", "totalHours": 8}
    ],
    "Allowance": [
        {"allowanceId": "A001", "allowanceName": "Travel", "eligibilityRule": "All employees"}
    ],

    # Workflow
    "MyPendingWorkflow": [
        {"wfRequestId": "WF001", "requestType": "Leave Request", "status": "Pending", "submittedBy": "EMP001"}
    ],
    "WfRequestParticipator": [
        {"wfRequestParticipatorId": 1, "wfRequestId": "WF001", "participatorId": "EMP002", "role": "Approver"}
    ],
    "WorkflowAllowedActionList": [
        {"wfRequestId": 1, "allowedAction": "Approve", "actionCode": "APPROVE"}
    ],
    "AlertMessage": [
        {"externalCode": "ALERT001", "message": "Pending approval required", "severity": "Medium"}
    ],
    "WfRequestComments": [
        {"wfRequestCommentId": 1, "wfRequestId": "WF001", "comment": "Please review", "commentBy": "EMP001"}
    ],
    "WfRequestStep": [
        {"wfRequestStepId": 1, "wfRequestId": "WF001", "stepNumber": 1, "stepName": "Manager Approval"}
    ],
    "AutoDelegateDetail": [
        {"AutoDelegateConfig_delegator": "EMP001", "externalCode": "AD001", "delegateTo": "EMP002"}
    ],
    "AutoDelegateConfig": [
        {"delegator": "EMP001", "isActive": True, "startDate": "2023-01-01"}
    ],
    "EmpWfRequest": [
        {"empWfRequestId": 1, "employeeId": "EMP001", "requestType": "Time Off", "status": "Submitted"}
    ],
    "WfRequest": [
        {"wfRequestId": 1, "requestType": "Leave", "currentStep": "Manager Review", "priority": "Normal"}
    ],

    # Compensation Information
    "OneTimeDeduction": [
        {"deductionId": "OTD001", "userId": "EMP001", "amount": 100, "reason": "Equipment damage"}
    ],
    "RecurringDeductionItem": [
        {"itemId": "RDI001", "deductionId": "RD001", "amount": 50, "frequency": "Monthly"}
    ],
    "EmpPayCompRecurring": [
        {"userId": "EMP001", "componentType": "Base Salary", "amount": 5000, "frequency": "Monthly"}
    ],
    "DeductionScreenId": [
        {"screenId": "DS001", "screenName": "Tax Deductions", "category": "Taxes"}
    ],
    "RecurringDeduction": [
        {"deductionId": "RD001", "deductionName": "Health Insurance", "amount": 200}
    ],
    "EmpCompensation": [
        {"userId": "EMP001", "baseSalary": 75000, "effectiveDate": "2023-01-01", "currency": "USD"}
    ],
    "EmpPayCompNonRecurring": [
        {"userId": "EMP001", "componentType": "Bonus", "amount": 5000, "payDate": "2023-12-15"}
    ],
    "EmpCompensationGroupSumCalculated": [
        {"userId": "EMP001", "groupType": "Total Compensation", "calculatedAmount": 80000}
    ],

    # Position Management
    "PositionRequisitionStatus": [
        {"requisitionId": "REQ001", "status": "Open", "positionTitle": "Software Engineer"}
    ],
    "PositionMatrixRelationship": [
        {"relationshipId": "PMR001", "positionId": "POS001", "matrixManagerId": "EMP002"}
    ],
    "Position": [
        {"positionId": "POS001", "positionTitle": "Senior Software Engineer", "department": "Engineering", "status": "Active"}
    ],
    "PositionRightToReturn": [
        {"positionId": "POS001", "employeeId": "EMP001", "rightToReturnDate": "2024-06-01"}
    ],

    # Dismissal Protection
    "EmployeeDismissalProtectionDetail": [
        {"detailId": "EDPD001", "userId": "EMP001", "protectionType": "Union Member", "effectiveDate": "2023-01-01"}
    ],
    "EmployeeDismissalProtection": [
        {"protectionId": "EDP001", "userId": "EMP001", "isProtected": True, "reason": "Maternity Leave"}
    ],

    # Apprentice Management
    "ApprenticeEventType": [
        {"eventTypeId": "AET001", "eventTypeName": "Training Completion", "category": "Education"}
    ],
    "DepartmentApprenticeDetail": [
        {"detailId": "DAD001", "departmentId": "DEPT001", "apprenticeId": "APP001", "program": "Software Development"}
    ],
    "ApprenticeSchool": [
        {"schoolId": "AS001", "schoolName": "Technical Institute", "location": "New York"}
    ],
    "ApprenticeGroup": [
        {"groupId": "AG001", "groupName": "2023 Cohort", "startDate": "2023-01-01"}
    ],
    "ApprenticeSchoolEvent": [
        {"eventId": "ASE001", "schoolId": "AS001", "eventType": "Graduation", "eventDate": "2023-12-15"}
    ],
    "ApprenticePracticalTrainingEvent": [
        {"eventId": "APTE001", "apprenticeId": "APP001", "trainingType": "On-the-job", "completionDate": "2023-06-01"}
    ],
    "ApprenticeInternalTrainingEvent": [
        {"eventId": "AITE001", "apprenticeId": "APP001", "trainingProgram": "Orientation", "completionDate": "2023-01-15"}
    ],
    "Apprentice": [
        {"apprenticeId": "APP001", "firstName": "Alex", "lastName": "Johnson", "program": "IT Support"}
    ],

    # Master Data Replication
    "EmployeeDataReplicationConfirmationErrorMessage": [
        {"messageId": "EDREM001", "errorCode": "E001", "errorMessage": "Invalid employee ID", "timestamp": "2023-12-01T10:00:00Z"}
    ],
    "EmployeeDataReplicationElement": [
        {"elementId": "EDRE001", "elementType": "Employee", "replicationStatus": "Success", "lastUpdated": "2023-12-01T09:00:00Z"}
    ],
    "EmployeeDataReplicationNotification": [
        {"notificationId": "EDRN001", "recipientId": "EMP001", "message": "Data sync completed", "sentDate": "2023-12-01T10:30:00Z"}
    ],
    "EmployeeDataReplicationConfirmation": [
        {"confirmationId": "EDRC001", "replicationId": "REP001", "status": "Confirmed", "confirmedBy": "SYSTEM"}
    ]
}

# Helper function to generate random mock data for entities
def generate_mock_entity(entity_name: str) -> Dict[str, Any]:
    """Generate a mock entity with basic fields."""
    base_entity = {
        "id": str(uuid.uuid4()),
        "createdDate": datetime.now().isoformat(),
        "lastModifiedDate": datetime.now().isoformat(),
        "status": "Active"
    }
    
    # Add entity-specific fields based on common patterns
    if "userId" in str(MOCK_DATA.get(entity_name, [])):
        base_entity["userId"] = f"EMP{random.randint(100, 999)}"
    
    if "externalCode" in str(MOCK_DATA.get(entity_name, [])):
        base_entity["externalCode"] = f"{entity_name.upper()}{random.randint(100, 999)}"
        
    return base_entity


@app.get("/successfactors/odata/v2/{entity}")
async def list_entities(entity: str):
    """List all entities of a given type."""
    data = MOCK_DATA.get(entity, [])
    if not data:
        # Generate mock data if entity not found
        data = [generate_mock_entity(entity)]
        MOCK_DATA[entity] = data
    return {"d": {"results": data}}


@app.post("/successfactors/odata/v2/{entity}")
async def create_entity(entity: str, request: Request):
    """Create a new entity."""
    payload = await request.json()
    
    # Initialize entity list if it doesn't exist
    if entity not in MOCK_DATA:
        MOCK_DATA[entity] = []
    
    # Add timestamps and ID if not present
    if "id" not in payload:
        payload["id"] = str(uuid.uuid4())
    if "createdDate" not in payload:
        payload["createdDate"] = datetime.now().isoformat()
    
    MOCK_DATA[entity].append(payload)
    return {"d": payload}


@app.get("/successfactors/odata/v2/{entity}({key})")
async def get_entity_by_single_key(entity: str, key: str):
    """Get entity by a single key (handles various key formats)."""
    data = MOCK_DATA.get(entity, [])
    
    # Clean the key (remove quotes if present)
    clean_key = key.strip("'\"")
    
    # Try to find the entity by different possible key fields
    possible_key_fields = ["userId", "code", "externalCode", "id", "backgroundElementId", 
                          "wfRequestId", "positionId", "apprenticeId", "skillId", "competencyId",
                          "roleId", "familyId", "certificationId", "profileId", "templateId"]
    
    for item in data:
        for key_field in possible_key_fields:
            if key_field in item and str(item[key_field]) == clean_key:
                return {"d": item}
    
    # If not found, generate a mock entity
    mock_entity = generate_mock_entity(entity)
    # Try to set the key field if we can determine it
    if entity.startswith("Background_"):
        mock_entity["backgroundElementId"] = int(clean_key) if clean_key.isdigit() else 1
        mock_entity["userId"] = f"EMP{random.randint(100, 999)}"
    elif "userId" in str(data):
        mock_entity["userId"] = clean_key
    elif "code" in str(data):
        mock_entity["code"] = clean_key
    elif "externalCode" in str(data):
        mock_entity["externalCode"] = clean_key
    
    return {"d": mock_entity}


@app.get("/successfactors/odata/v2/{entity}({key1},{key2})")
async def get_entity_by_two_keys(entity: str, key1: str, key2: str):
    """Get entity by two keys (common for background entities and others)."""
    data = MOCK_DATA.get(entity, [])
    
    # Clean the keys
    clean_key1 = key1.split("=")[1].strip("'\"") if "=" in key1 else key1.strip("'\"")
    clean_key2 = key2.split("=")[1].strip("'\"") if "=" in key2 else key2.strip("'\"")
    
    # For background entities, typically backgroundElementId and userId
    for item in data:
        if (str(item.get("backgroundElementId", "")) == clean_key1 and 
            str(item.get("userId", "")) == clean_key2) or \
           (str(item.get("userId", "")) == clean_key1 and 
            str(item.get("backgroundElementId", "")) == clean_key2):
            return {"d": item}
    
    # Generate mock entity if not found
    mock_entity = generate_mock_entity(entity)
    if entity.startswith("Background_"):
        mock_entity["backgroundElementId"] = int(clean_key1) if clean_key1.isdigit() else int(clean_key2) if clean_key2.isdigit() else 1
        mock_entity["userId"] = clean_key2 if not clean_key2.isdigit() else clean_key1
    
    return {"d": mock_entity}


@app.get("/successfactors/odata/v2/{entity}({key1},{key2},{key3})")
async def get_entity_by_three_keys(entity: str, key1: str, key2: str, key3: str):
    """Get entity by three keys."""
    data = MOCK_DATA.get(entity, [])
    
    # Clean the keys
    clean_key1 = key1.split("=")[1].strip("'\"") if "=" in key1 else key1.strip("'\"")
    clean_key2 = key2.split("=")[1].strip("'\"") if "=" in key2 else key2.strip("'\"")
    clean_key3 = key3.split("=")[1].strip("'\"") if "=" in key3 else key3.strip("'\"")
    
    # Try to find matching entity
    for item in data:
        # This is a simplified match - in practice, you'd want to parse the key names
        if (str(item.get("EmpCostDistribution_effectiveStartDate", "")) == clean_key1 and
            str(item.get("EmpCostDistribution_usersSysId", "")) == clean_key2 and
            str(item.get("externalCode", "")) == clean_key3):
            return {"d": item}
    
    # Generate mock entity
    mock_entity = generate_mock_entity(entity)
    mock_entity["key1"] = clean_key1
    mock_entity["key2"] = clean_key2  
    mock_entity["key3"] = clean_key3
    return {"d": mock_entity}


@app.put("/successfactors/odata/v2/{entity}({key})")
async def update_entity_by_single_key(entity: str, key: str, request: Request):
    """Update entity by single key."""
    payload = await request.json()
    data = MOCK_DATA.get(entity, [])
    clean_key = key.strip("'\"")
    
    # Find and update the entity
    possible_key_fields = ["userId", "code", "externalCode", "id", "backgroundElementId"]
    
    for i, item in enumerate(data):
        for key_field in possible_key_fields:
            if key_field in item and str(item[key_field]) == clean_key:
                # Update the item
                data[i].update(payload)
                data[i]["lastModifiedDate"] = datetime.now().isoformat()
                return {"status": "Updated"}
    
    return JSONResponse(status_code=404, content={"error": "Entity not found"})


@app.put("/successfactors/odata/v2/{entity}({key1},{key2})")
async def update_entity_by_two_keys(entity: str, key1: str, key2: str, request: Request):
    """Update entity by two keys."""
    payload = await request.json()
    data = MOCK_DATA.get(entity, [])
    
    clean_key1 = key1.split("=")[1].strip("'\"") if "=" in key1 else key1.strip("'\"")
    clean_key2 = key2.split("=")[1].strip("'\"") if "=" in key2 else key2.strip("'\"")
    
    for i, item in enumerate(data):
        if ((str(item.get("backgroundElementId", "")) == clean_key1 and 
             str(item.get("userId", "")) == clean_key2) or
            (str(item.get("userId", "")) == clean_key1 and 
             str(item.get("backgroundElementId", "")) == clean_key2)):
            data[i].update(payload)
            data[i]["lastModifiedDate"] = datetime.now().isoformat()
            return {"status": "Updated"}
    
    return JSONResponse(status_code=404, content={"error": "Entity not found"})


@app.delete("/successfactors/odata/v2/{entity}({key})")
async def delete_entity_by_single_key(entity: str, key: str):
    """Delete entity by single key."""
    data = MOCK_DATA.get(entity, [])
    clean_key = key.strip("'\"")
    initial_len = len(data)
    
    # Remove entities that match the key
    possible_key_fields = ["userId", "code", "externalCode", "id", "backgroundElementId"]
    
    MOCK_DATA[entity] = [
        item for item in data 
        if not any(str(item.get(key_field, "")) == clean_key for key_field in possible_key_fields)
    ]
    
    if len(MOCK_DATA[entity]) < initial_len:
        return {"d": {"status": "Deleted"}}
    return JSONResponse(status_code=404, content={"error": "Entity not found"})


@app.delete("/successfactors/odata/v2/{entity}({key1},{key2})")
async def delete_entity_by_two_keys(entity: str, key1: str, key2: str):
    """Delete entity by two keys."""
    data = MOCK_DATA.get(entity, [])
    clean_key1 = key1.split("=")[1].strip("'\"") if "=" in key1 else key1.strip("'\"")
    clean_key2 = key2.split("=")[1].strip("'\"") if "=" in key2 else key2.strip("'\"")
    initial_len = len(data)
    
    MOCK_DATA[entity] = [
        item for item in data 
        if not ((str(item.get("backgroundElementId", "")) == clean_key1 and 
                 str(item.get("userId", "")) == clean_key2) or
                (str(item.get("userId", "")) == clean_key1 and 
                 str(item.get("backgroundElementId", "")) == clean_key2))
    ]
    
    if len(MOCK_DATA[entity]) < initial_len:
        return {"d": {"status": "Deleted"}}
    return JSONResponse(status_code=404, content={"error": "Entity not found"})


# Legacy endpoints for backward compatibility
@app.post("/successfactors/odata/v2/HireDateChange")
async def create_hire_date_change(request: Request):
    """Legacy endpoint for HireDateChange creation."""
    return await create_entity("HireDateChange", request)


@app.delete("/successfactors/odata/v2/HireDateChange('{code}')")
async def delete_hire_date_change(code: str):
    """Legacy endpoint for HireDateChange deletion."""
    return await delete_entity_by_single_key("HireDateChange", code)


# Workflow action endpoints
@app.post("/successfactors/odata/v2/approveWfRequest")
async def approve_workflow_request(request: Request):
    """Approve a workflow request."""
    params = await request.json() if hasattr(request, 'json') else {}
    return {"d": {"result": "Workflow approved", "status": "Success"}}


@app.post("/successfactors/odata/v2/rejectWfRequest")
async def reject_workflow_request(request: Request):
    """Reject a workflow request."""
    params = await request.json() if hasattr(request, 'json') else {}
    return {"d": {"result": "Workflow rejected", "status": "Success"}}


@app.post("/successfactors/odata/v2/commentWfRequest")
async def comment_workflow_request(request: Request):
    """Add comment to workflow request."""
    params = await request.json() if hasattr(request, 'json') else {}
    return {"d": {"result": "Comment added", "status": "Success"}}


@app.post("/successfactors/odata/v2/sendbackWfRequest")
async def sendback_workflow_request(request: Request):
    """Send back a workflow request."""
    params = await request.json() if hasattr(request, 'json') else {}
    return {"d": {"result": "Workflow sent back", "status": "Success"}}


@app.post("/successfactors/odata/v2/withdrawWfRequest")
async def withdraw_workflow_request(request: Request):
    """Withdraw a workflow request."""
    params = await request.json() if hasattr(request, 'json') else {}
    return {"d": {"result": "Workflow withdrawn", "status": "Success"}}


@app.post("/successfactors/odata/v2/getWorkflowPendingData")
async def get_workflow_pending_data(request: Request):
    """Get pending workflow data."""
    params = await request.json() if hasattr(request, 'json') else {}
    return {"d": {"result": {"pendingItems": [], "totalCount": 0}, "status": "Success"}}


# Special endpoint for Position management
@app.get("/successfactors/odata/v2/getPositionObjectData")
async def get_position_object_data():
    """Get position object data."""
    return {"d": {"result": MOCK_DATA.get("Position", [])}}


@app.middleware("http")
async def add_content_type_header(request: Request, call_next):
    """Add content type header to all responses."""
    response = await call_next(request)
    response.headers["Content-Type"] = "application/json"
    return response


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "supported_entities": len(MOCK_DATA)}


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting SAP SuccessFactors Employee Central Mock Server...")
    print(f"📊 Supporting {len(MOCK_DATA)} entity types")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000)
