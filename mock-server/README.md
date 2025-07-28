# SAP SuccessFactors Employee Central Mock Server

This mock server provides comprehensive support for all SAP SuccessFactors Employee Central APIs used by the Ballerina connectors.

## Features

- **Complete API Coverage**: Supports all entities from all Ballerina client modules:
  - Employment Information (ecemploymentinformation)
  - Employee Profile (ecemployeeprofile) 
  - Skills Management (ecskillsmanagement)
  - Payroll & Timesheets (ecpayrolltimesheets)
  - Workflow (ecworkflow)
  - Compensation Information (eccompensationinformation)
  - Position Management (ecpositionmanagement)
  - Dismissal Protection (ecdismissalprotection)
  - Apprentice Management (ecapprenticemanagement)
  - Master Data Replication (ecmasterdatareplication)
  - Alternative Cost Distribution (ecalternativecostdistribution)

- **Dynamic Entity Support**: Automatically generates mock data for any entity not explicitly defined
- **Multiple Key Support**: Handles single, double, and triple key entity lookups
- **Full CRUD Operations**: Supports Create, Read, Update, Delete operations
- **Workflow Actions**: Supports workflow approval, rejection, comments, etc.
- **OData Compliance**: Follows OData v2 response format

## Supported Entities

### Employment Information
- EmpEmployment, EmpJob, EmpBeneficiary, EmpEmploymentTermination
- EmpPensionPayout, EmpWorkPermit, EmpJobRelationships
- PersonEmpTerminationInfo, HireDateChange

### Employee Profile (Background entities)
- Background_Community, Background_Courses, Background_Benefitselection
- Background_OutsideWorkExperience, Background_Promotability
- Background_Fsaelection, Background_Compensation, Background_Memberships
- Background_Documents, Background_FuncExperience, Background_TalentPool
- Background_Awards, Background_Education, Background_Mobility
- Background_VarPayEmpHistData, Background_InsideWorkExperience
- Background_PreferredNextMove, Background_Googledocs
- UserBadges, BadgeTemplates, EPPublicProfile

### Skills Management
- SkillEntity, CompetencyEntity, RoleEntity, FamilyEntity
- JobProfile, PositionEntity, CertificationEntity
- JobResponsibilityEntity, InterviewQuestionEntity
- Various mapping entities (RoleSkillMapping, PositionCompetencyMapping, etc.)

### Payroll & Timesheets
- EmployeeTimeSheet, ExternalAllowance, TimeCollector
- ExternalTimeRecord, ExternalTimeData, DataReplicationProxy
- EmployeeTimeSheetEntry, TimeRecording, Allowance

### Workflow
- MyPendingWorkflow, WfRequest, WfRequestParticipator
- WorkflowAllowedActionList, AlertMessage, WfRequestComments
- AutoDelegateConfig, AutoDelegateDetail, EmpWfRequest

### And many more...

## Running the Mock Server

### Prerequisites
```bash
pip install fastapi uvicorn
```

### Start the Server
```bash
cd mock-server
python -m uvicorn server:app --reload --port 8000
```

The server will be available at `http://localhost:8000`

## API Examples

### List Entities
```http
GET /successfactors/odata/v2/EmpEmployment
```

### Get Entity by Single Key
```http
GET /successfactors/odata/v2/EmpEmployment('EMP001')
GET /successfactors/odata/v2/HireDateChange('HDC001')
```

### Get Entity by Multiple Keys (Background entities)
```http
GET /successfactors/odata/v2/Background_Education(backgroundElementId=1,userId='EMP001')
```

### Create Entity
```http
POST /successfactors/odata/v2/EmpEmployment
Content-Type: application/json

{
  "userId": "EMP003",  
  "startDate": "2024-01-01",
  "employmentStatus": "Active"
}
```

### Update Entity
```http
PUT /successfactors/odata/v2/EmpEmployment('EMP001')
Content-Type: application/json

{
  "employmentStatus": "Inactive"
}
```

### Delete Entity
```http
DELETE /successfactors/odata/v2/EmpEmployment('EMP001')
```

### Workflow Actions
```http
POST /successfactors/odata/v2/approveWfRequest
POST /successfactors/odata/v2/rejectWfRequest
POST /successfactors/odata/v2/commentWfRequest
```

## Configuration

### Connecting Ballerina Clients
Configure your Ballerina clients to use the mock server:

```ballerina
Client client = check new({
    auth: {
        username: "testuser",
        password: "testpass"
    }
}, "localhost", 8000);
```

### Custom Mock Data
You can modify the `MOCK_DATA` dictionary in `server.py` to add your own test data for specific entities.

## Health Check
```http
GET /health
```

Returns server status and the number of supported entities.

## Dynamic Entity Support

If you request an entity that's not explicitly defined in `MOCK_DATA`, the server will:
1. Generate a mock entity with common fields (id, timestamps, status)
2. Add entity-specific fields based on common patterns
3. Store it for future requests

This ensures all Ballerina client operations work even for newly added entities.
