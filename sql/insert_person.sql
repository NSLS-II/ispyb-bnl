-- Create a test person
INSERT INTO Person (familyName, givenName, title, login) VALUES ('User', 'Test', 'Mr', 'ispybtest');

-- See relevant columns for all Persons
SELECT personId, familyName, givenName, title, login FROM Person;

-- See relevant columns for all BLSessions
SELECT sessionId, proposalId, beamLineName FROM BLSession;

-- Create BLSession - Person associations 
INSERT INTO Session_has_Person (sessionId, personId, role) VALUES (55167, 46270, 'Team Member');
INSERT INTO Session_has_Person (sessionId, personId, role) VALUES (55168, 46270, 'Team Member');
INSERT INTO Session_has_Person (sessionId, personId, role) VALUES (339525, 46270, 'Team Member');
INSERT INTO Session_has_Person (sessionId, personId, role) VALUES (339532, 46270, 'Team Member');
