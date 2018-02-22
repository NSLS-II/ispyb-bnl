INSERT INTO Person (familyName, givenName, title, login) VALUES ('User', 'Test', 'Mr', 'ispybtest');

SELECT personId, familyName, givenName, title, login FROM Person; 

SELECT sessionId, proposalId, beamLineName FROM BLSession;

INSERT INTO Session_has_Person (sessionId, personId, role) VALUES (55167, 46270, 'Team Member');

INSERT INTO Session_has_Person (sessionId, personId, role) VALUES (55168, 46270, 'Team Member');

INSERT INTO Session_has_Person (sessionId, personId, role) VALUES (339525, 46270, 'Team Member');

INSERT INTO Session_has_Person (sessionId, personId, role) VALUES (339532, 46270, 'Team Member');

