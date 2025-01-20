# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/server/v1/team.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chalk._gen.chalk.auth.v1 import agent_pb2 as chalk_dot_auth_dot_v1_dot_agent__pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as chalk_dot_auth_dot_v1_dot_audit__pb2
from chalk._gen.chalk.auth.v1 import displayagent_pb2 as chalk_dot_auth_dot_v1_dot_displayagent__pb2
from chalk._gen.chalk.auth.v1 import featurepermission_pb2 as chalk_dot_auth_dot_v1_dot_featurepermission__pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as chalk_dot_auth_dot_v1_dot_permissions__pb2
from chalk._gen.chalk.server.v1 import environment_pb2 as chalk_dot_server_dot_v1_dot_environment__pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as chalk_dot_utils_dot_v1_dot_sensitive__pb2
from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1a\x63halk/server/v1/team.proto\x12\x0f\x63halk.server.v1\x1a\x19\x63halk/auth/v1/agent.proto\x1a\x19\x63halk/auth/v1/audit.proto\x1a chalk/auth/v1/displayagent.proto\x1a%chalk/auth/v1/featurepermission.proto\x1a\x1f\x63halk/auth/v1/permissions.proto\x1a!chalk/server/v1/environment.proto\x1a\x1e\x63halk/utils/v1/sensitive.proto\x1a google/protobuf/descriptor.proto\x1a google/protobuf/field_mask.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\x0f\n\rGetEnvRequest"P\n\x0eGetEnvResponse\x12>\n\x0b\x65nvironment\x18\x01 \x01(\x0b\x32\x1c.chalk.server.v1.EnvironmentR\x0b\x65nvironment"2\n\x16GetEnvironmentsRequest\x12\x18\n\x07project\x18\x01 \x01(\tR\x07project"[\n\x17GetEnvironmentsResponse\x12@\n\x0c\x65nvironments\x18\x02 \x03(\x0b\x32\x1c.chalk.server.v1.EnvironmentR\x0c\x65nvironments"\x11\n\x0fGetAgentRequest">\n\x10GetAgentResponse\x12*\n\x05\x61gent\x18\x01 \x01(\x0b\x32\x14.chalk.auth.v1.AgentR\x05\x61gent"\x18\n\x16GetDisplayAgentRequest"L\n\x17GetDisplayAgentResponse\x12\x31\n\x05\x61gent\x18\x01 \x01(\x0b\x32\x1b.chalk.auth.v1.DisplayAgentR\x05\x61gent"\x82\x03\n\x04Team\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12\x12\n\x04slug\x18\x03 \x01(\tR\x04slug\x12\x17\n\x04logo\x18\x04 \x01(\tH\x00R\x04logo\x88\x01\x01\x12\x34\n\x08projects\x18\x05 \x03(\x0b\x32\x18.chalk.server.v1.ProjectR\x08projects\x12(\n\rscim_provider\x18\x06 \x01(\tH\x01R\x0cscimProvider\x88\x01\x01\x12S\n\x10spec_config_json\x18\x07 \x03(\x0b\x32).chalk.server.v1.Team.SpecConfigJsonEntryR\x0especConfigJson\x1aY\n\x13SpecConfigJsonEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.ValueR\x05value:\x02\x38\x01\x42\x07\n\x05_logoB\x10\n\x0e_scim_provider"\xb5\x01\n\x07Project\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x17\n\x07team_id\x18\x02 \x01(\tR\x06teamId\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x12@\n\x0c\x65nvironments\x18\x04 \x03(\x0b\x32\x1c.chalk.server.v1.EnvironmentR\x0c\x65nvironments\x12\x1e\n\x08git_repo\x18\x05 \x01(\tH\x00R\x07gitRepo\x88\x01\x01\x42\x0b\n\t_git_repo"]\n\x11\x43reateTeamRequest\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x12\n\x04slug\x18\x02 \x01(\tR\x04slug\x12\x17\n\x04logo\x18\x03 \x01(\tH\x00R\x04logo\x88\x01\x01\x42\x07\n\x05_logo"?\n\x12\x43reateTeamResponse\x12)\n\x04team\x18\x01 \x01(\x0b\x32\x15.chalk.server.v1.TeamR\x04team"*\n\x14\x43reateProjectRequest\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name"K\n\x15\x43reateProjectResponse\x12\x32\n\x07project\x18\x01 \x01(\x0b\x32\x18.chalk.server.v1.ProjectR\x07project"l\n\x18\x43reateEnvironmentRequest\x12\x1d\n\nproject_id\x18\x01 \x01(\tR\tprojectId\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12\x1d\n\nis_default\x18\x03 \x01(\x08R\tisDefault"[\n\x19\x43reateEnvironmentResponse\x12>\n\x0b\x65nvironment\x18\x01 \x01(\x0b\x32\x1c.chalk.server.v1.EnvironmentR\x0b\x65nvironment"\x9d\x02\n\x1aUpdateEnvironmentOperation\x12/\n\x11specs_config_json\x18\x01 \x01(\tH\x00R\x0fspecsConfigJson\x88\x01\x01\x12r\n\x13\x61\x64\x64itional_env_vars\x18\x02 \x03(\x0b\x32\x42.chalk.server.v1.UpdateEnvironmentOperation.AdditionalEnvVarsEntryR\x11\x61\x64\x64itionalEnvVars\x1a\x44\n\x16\x41\x64\x64itionalEnvVarsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x42\x14\n\x12_specs_config_json"\xac\x01\n\x18UpdateEnvironmentRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x43\n\x06update\x18\x02 \x01(\x0b\x32+.chalk.server.v1.UpdateEnvironmentOperationR\x06update\x12;\n\x0bupdate_mask\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.FieldMaskR\nupdateMask"[\n\x19UpdateEnvironmentResponse\x12>\n\x0b\x65nvironment\x18\x01 \x01(\x0b\x32\x1c.chalk.server.v1.EnvironmentR\x0b\x65nvironment"\x10\n\x0eGetTeamRequest"<\n\x0fGetTeamResponse\x12)\n\x04team\x18\x01 \x01(\x0b\x32\x15.chalk.server.v1.TeamR\x04team"\xcb\x03\n\x19\x43reateServiceTokenRequest\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12;\n\x0bpermissions\x18\x02 \x03(\x0e\x32\x19.chalk.auth.v1.PermissionR\x0bpermissions\x12\'\n\rcustom_claims\x18\x03 \x03(\tB\x02\x18\x01R\x0c\x63ustomClaims\x12\x43\n\x0f\x63ustomer_claims\x18\x04 \x03(\x0b\x32\x1a.chalk.auth.v1.CustomClaimR\x0e\x63ustomerClaims\x12\x81\x01\n\x19\x66\x65\x61ture_tag_to_permission\x18\x05 \x03(\x0b\x32\x46.chalk.server.v1.CreateServiceTokenRequest.FeatureTagToPermissionEntryR\x16\x66\x65\x61tureTagToPermission\x1ak\n\x1b\x46\x65\x61tureTagToPermissionEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x36\n\x05value\x18\x02 \x01(\x0e\x32 .chalk.auth.v1.FeaturePermissionR\x05value:\x02\x38\x01"\x7f\n\x1a\x43reateServiceTokenResponse\x12\x36\n\x05\x61gent\x18\x01 \x01(\x0b\x32 .chalk.auth.v1.ServiceTokenAgentR\x05\x61gent\x12)\n\rclient_secret\x18\x02 \x01(\tB\x04\xd8\xa1\'\x01R\x0c\x63lientSecret"+\n\x19\x44\x65leteServiceTokenRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id"\x1c\n\x1a\x44\x65leteServiceTokenResponse"\xd7\x01\n\x15PermissionDescription\x12)\n\x02id\x18\x01 \x01(\x0e\x32\x19.chalk.auth.v1.PermissionR\x02id\x12\x12\n\x04slug\x18\x02 \x01(\tR\x04slug\x12\x1c\n\tnamespace\x18\x03 \x01(\tR\tnamespace\x12\x12\n\x04name\x18\x04 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x05 \x01(\tR\x0b\x64\x65scription\x12+\n\x11group_description\x18\x06 \x01(\tR\x10groupDescription"\x87\x02\n\x0fRoleDescription\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x03 \x01(\tR\x0b\x64\x65scription\x12;\n\x0bpermissions\x18\x04 \x03(\x0e\x32\x19.chalk.auth.v1.PermissionR\x0bpermissions\x12R\n\x13\x66\x65\x61ture_permissions\x18\x05 \x01(\x0b\x32!.chalk.auth.v1.FeaturePermissionsR\x12\x66\x65\x61turePermissions\x12\x1d\n\nis_default\x18\x06 \x01(\x08R\tisDefault" \n\x1eGetAvailablePermissionsRequest"\x8d\x02\n\x1fGetAvailablePermissionsResponse\x12H\n\x0bpermissions\x18\x01 \x03(\x0b\x32&.chalk.server.v1.PermissionDescriptionR\x0bpermissions\x12\x36\n\x05roles\x18\x02 \x03(\x0b\x32 .chalk.server.v1.RoleDescriptionR\x05roles\x12h\n#available_service_token_permissions\x18\x03 \x03(\x0e\x32\x19.chalk.auth.v1.PermissionR availableServiceTokenPermissions"z\n\x1fUpsertFeaturePermissionsRequest\x12\x12\n\x04role\x18\x01 \x01(\tR\x04role\x12\x43\n\x0bpermissions\x18\x02 \x01(\x0b\x32!.chalk.auth.v1.FeaturePermissionsR\x0bpermissions"{\n UpsertFeaturePermissionsResponse\x12\x12\n\x04role\x18\x01 \x01(\tR\x04role\x12\x43\n\x0bpermissions\x18\x02 \x01(\x0b\x32!.chalk.auth.v1.FeaturePermissionsR\x0bpermissions"\x1a\n\x18ListServiceTokensRequest"\\\n\x19ListServiceTokensResponse\x12?\n\x06\x61gents\x18\x01 \x03(\x0b\x32\'.chalk.auth.v1.DisplayServiceTokenAgentR\x06\x61gents"\xbf\x03\n\x19UpdateServiceTokenRequest\x12\x1b\n\tclient_id\x18\x01 \x01(\tR\x08\x63lientId\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12;\n\x0bpermissions\x18\x03 \x03(\x0e\x32\x19.chalk.auth.v1.PermissionR\x0bpermissions\x12\x43\n\x0f\x63ustomer_claims\x18\x04 \x03(\x0b\x32\x1a.chalk.auth.v1.CustomClaimR\x0e\x63ustomerClaims\x12\x81\x01\n\x19\x66\x65\x61ture_tag_to_permission\x18\x05 \x03(\x0b\x32\x46.chalk.server.v1.UpdateServiceTokenRequest.FeatureTagToPermissionEntryR\x16\x66\x65\x61tureTagToPermission\x1ak\n\x1b\x46\x65\x61tureTagToPermissionEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x36\n\x05value\x18\x02 \x01(\x0e\x32 .chalk.auth.v1.FeaturePermissionR\x05value:\x02\x38\x01"[\n\x1aUpdateServiceTokenResponse\x12=\n\x05\x61gent\x18\x01 \x01(\x0b\x32\'.chalk.auth.v1.DisplayServiceTokenAgentR\x05\x61gent"U\n\x1eUpdateScimGroupSettingsRequest\x12\x1d\n\nquery_tags\x18\x01 \x03(\tR\tqueryTags\x12\x14\n\x05group\x18\x02 \x01(\tR\x05group"@\n\x1fUpdateScimGroupSettingsResponse\x12\x1d\n\nquery_tags\x18\x01 \x03(\tR\tqueryTags"Y\n\x17InviteTeamMemberRequest\x12\x14\n\x05\x65mail\x18\x01 \x01(\tR\x05\x65mail\x12\x1c\n\x07role_id\x18\x02 \x01(\tH\x00R\x06roleId\x88\x01\x01\x42\n\n\x08_role_id"\x1a\n\x18InviteTeamMemberResponse")\n\x17\x45xpireTeamInviteRequest\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id"\x1a\n\x18\x45xpireTeamInviteResponse"\xa3\x01\n\nTeamInvite\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x14\n\x05\x65mail\x18\x02 \x01(\tR\x05\x65mail\x12\x12\n\x04team\x18\x03 \x01(\tR\x04team\x12\x17\n\x04role\x18\x04 \x01(\tH\x00R\x04role\x88\x01\x01\x12\x39\n\ncreated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAtB\x07\n\x05_role"\x18\n\x16ListTeamInvitesRequest"P\n\x17ListTeamInvitesResponse\x12\x35\n\x07invites\x18\x01 \x03(\x0b\x32\x1b.chalk.server.v1.TeamInviteR\x07invites"h\n\tScimGroup\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x18\n\x07\x64isplay\x18\x02 \x01(\tR\x07\x64isplay\x12\x17\n\x07team_id\x18\x03 \x01(\tR\x06teamId\x12\x18\n\x07members\x18\x04 \x03(\tR\x07members"\x93\x01\n\x17ScimGroupRoleAssignment\x12\x19\n\x08group_id\x18\x01 \x01(\tR\x07groupId\x12%\n\x0e\x65nvironment_id\x18\x03 \x01(\tR\renvironmentId\x12\x17\n\x07role_id\x18\x04 \x01(\tR\x06roleId\x12\x1d\n\nquery_tags\x18\x05 \x03(\tR\tqueryTags"A\n\x12UserRoleAssignment\x12\x17\n\x07role_id\x18\x01 \x01(\tR\x06roleId\x12\x12\n\x04type\x18\x02 \x01(\tR\x04type"\xdb\x01\n\x0fUserPermissions\x12\x17\n\x07user_id\x18\x01 \x01(\tR\x06userId\x12%\n\x0e\x65nvironment_id\x18\x02 \x01(\tR\renvironmentId\x12\x42\n\nuser_roles\x18\x03 \x03(\x0b\x32#.chalk.server.v1.UserRoleAssignmentR\tuserRoles\x12\x44\n\x10user_permissions\x18\x04 \x03(\x0e\x32\x19.chalk.auth.v1.PermissionR\x0fuserPermissions"\x87\x02\n\x04User\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x17\n\x04name\x18\x02 \x01(\tH\x00R\x04name\x88\x01\x01\x12\x19\n\x05\x65mail\x18\x03 \x01(\tH\x01R\x05\x65mail\x88\x01\x01\x12\x19\n\x05image\x18\x04 \x01(\tH\x02R\x05image\x88\x01\x01\x12\x1c\n\x07team_id\x18\x05 \x01(\tH\x03R\x06teamId\x88\x01\x01\x12\x46\n\x0e\x64\x65\x61\x63tivated_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x04R\rdeactivatedAt\x88\x01\x01\x42\x07\n\x05_nameB\x08\n\x06_emailB\x08\n\x06_imageB\n\n\x08_team_idB\x11\n\x0f_deactivated_at"\xd5\x01\n\x16\x45nvironmentPermissions\x12%\n\x0e\x65nvironment_id\x18\x01 \x01(\tR\renvironmentId\x12G\n\nscim_roles\x18\x02 \x03(\x0b\x32(.chalk.server.v1.ScimGroupRoleAssignmentR\tscimRoles\x12K\n\x10user_permissions\x18\x03 \x03(\x0b\x32 .chalk.server.v1.UserPermissionsR\x0fuserPermissions"\x1b\n\x19GetTeamPermissionsRequest"\xad\x02\n\x1aGetTeamPermissionsResponse\x12\x36\n\x05roles\x18\x01 \x03(\x0b\x32 .chalk.server.v1.RoleDescriptionR\x05roles\x12;\n\x0bscim_groups\x18\x02 \x03(\x0b\x32\x1a.chalk.server.v1.ScimGroupR\nscimGroups\x12`\n\x17\x65nvironment_permissions\x18\x03 \x03(\x0b\x32\'.chalk.server.v1.EnvironmentPermissionsR\x16\x65nvironmentPermissions\x12\x38\n\x0cteam_members\x18\x04 \x03(\x0b\x32\x15.chalk.server.v1.UserR\x0bteamMembers2\x82\x12\n\x0bTeamService\x12Q\n\x06GetEnv\x12\x1e.chalk.server.v1.GetEnvRequest\x1a\x1f.chalk.server.v1.GetEnvResponse"\x06\x90\x02\x01\x80}\x0b\x12l\n\x0fGetEnvironments\x12\'.chalk.server.v1.GetEnvironmentsRequest\x1a(.chalk.server.v1.GetEnvironmentsResponse"\x06\x90\x02\x01\x80}\x02\x12W\n\x08GetAgent\x12 .chalk.server.v1.GetAgentRequest\x1a!.chalk.server.v1.GetAgentResponse"\x06\x90\x02\x01\x80}\x02\x12l\n\x0fGetDisplayAgent\x12\'.chalk.server.v1.GetDisplayAgentRequest\x1a(.chalk.server.v1.GetDisplayAgentResponse"\x06\x90\x02\x01\x80}\x02\x12T\n\x07GetTeam\x12\x1f.chalk.server.v1.GetTeamRequest\x1a .chalk.server.v1.GetTeamResponse"\x06\x90\x02\x01\x80}\x02\x12`\n\nCreateTeam\x12".chalk.server.v1.CreateTeamRequest\x1a#.chalk.server.v1.CreateTeamResponse"\t\x80}\x1b\x8a\xd3\x0e\x02\x08\x02\x12i\n\rCreateProject\x12%.chalk.server.v1.CreateProjectRequest\x1a&.chalk.server.v1.CreateProjectResponse"\t\x80}\x1a\x8a\xd3\x0e\x02\x08\x02\x12u\n\x11\x43reateEnvironment\x12).chalk.server.v1.CreateEnvironmentRequest\x1a*.chalk.server.v1.CreateEnvironmentResponse"\t\x80}\x1a\x8a\xd3\x0e\x02\x08\x02\x12u\n\x11UpdateEnvironment\x12).chalk.server.v1.UpdateEnvironmentRequest\x1a*.chalk.server.v1.UpdateEnvironmentResponse"\t\x80}\x0c\x8a\xd3\x0e\x02\x08\x02\x12\x84\x01\n\x17GetAvailablePermissions\x12/.chalk.server.v1.GetAvailablePermissionsRequest\x1a\x30.chalk.server.v1.GetAvailablePermissionsResponse"\x06\x90\x02\x01\x80}\x02\x12\x8f\x01\n\x12\x43reateServiceToken\x12*.chalk.server.v1.CreateServiceTokenRequest\x1a+.chalk.server.v1.CreateServiceTokenResponse" \x80}\x15\x8a\xd3\x0e\x19\x08\x02\x12\x15\x43reated service token\x12x\n\x12\x44\x65leteServiceToken\x12*.chalk.server.v1.DeleteServiceTokenRequest\x1a+.chalk.server.v1.DeleteServiceTokenResponse"\t\x80}\x15\x8a\xd3\x0e\x02\x08\x02\x12o\n\x11ListServiceTokens\x12).chalk.server.v1.ListServiceTokensRequest\x1a*.chalk.server.v1.ListServiceTokensResponse"\x03\x80}\x16\x12x\n\x12UpdateServiceToken\x12*.chalk.server.v1.UpdateServiceTokenRequest\x1a+.chalk.server.v1.UpdateServiceTokenResponse"\t\x80}\x15\x8a\xd3\x0e\x02\x08\x02\x12r\n\x10InviteTeamMember\x12(.chalk.server.v1.InviteTeamMemberRequest\x1a).chalk.server.v1.InviteTeamMemberResponse"\t\x80}\x07\x8a\xd3\x0e\x02\x08\x02\x12r\n\x10\x45xpireTeamInvite\x12(.chalk.server.v1.ExpireTeamInviteRequest\x1a).chalk.server.v1.ExpireTeamInviteResponse"\t\x80}\x08\x8a\xd3\x0e\x02\x08\x02\x12i\n\x0fListTeamInvites\x12\'.chalk.server.v1.ListTeamInvitesRequest\x1a(.chalk.server.v1.ListTeamInvitesResponse"\x03\x80}\t\x12\x8a\x01\n\x18UpsertFeaturePermissions\x12\x30.chalk.server.v1.UpsertFeaturePermissionsRequest\x1a\x31.chalk.server.v1.UpsertFeaturePermissionsResponse"\t\x80}\x15\x8a\xd3\x0e\x02\x08\x02\x12\x87\x01\n\x17UpdateScimGroupSettings\x12/.chalk.server.v1.UpdateScimGroupSettingsRequest\x1a\x30.chalk.server.v1.UpdateScimGroupSettingsResponse"\t\x80}\n\x8a\xd3\x0e\x02\x08\x02\x12r\n\x12GetTeamPermissions\x12*.chalk.server.v1.GetTeamPermissionsRequest\x1a+.chalk.server.v1.GetTeamPermissionsResponse"\x03\x80}\x02\x42\x92\x01\n\x13\x63om.chalk.server.v1B\tTeamProtoP\x01Z\x12server/v1;serverv1\xa2\x02\x03\x43SX\xaa\x02\x0f\x43halk.Server.V1\xca\x02\x0f\x43halk\\Server\\V1\xe2\x02\x1b\x43halk\\Server\\V1\\GPBMetadata\xea\x02\x11\x43halk::Server::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "chalk.server.v1.team_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\023com.chalk.server.v1B\tTeamProtoP\001Z\022server/v1;serverv1\242\002\003CSX\252\002\017Chalk.Server.V1\312\002\017Chalk\\Server\\V1\342\002\033Chalk\\Server\\V1\\GPBMetadata\352\002\021Chalk::Server::V1"
    _globals["_TEAM_SPECCONFIGJSONENTRY"]._options = None
    _globals["_TEAM_SPECCONFIGJSONENTRY"]._serialized_options = b"8\001"
    _globals["_UPDATEENVIRONMENTOPERATION_ADDITIONALENVVARSENTRY"]._options = None
    _globals["_UPDATEENVIRONMENTOPERATION_ADDITIONALENVVARSENTRY"]._serialized_options = b"8\001"
    _globals["_CREATESERVICETOKENREQUEST_FEATURETAGTOPERMISSIONENTRY"]._options = None
    _globals["_CREATESERVICETOKENREQUEST_FEATURETAGTOPERMISSIONENTRY"]._serialized_options = b"8\001"
    _globals["_CREATESERVICETOKENREQUEST"].fields_by_name["custom_claims"]._options = None
    _globals["_CREATESERVICETOKENREQUEST"].fields_by_name["custom_claims"]._serialized_options = b"\030\001"
    _globals["_CREATESERVICETOKENRESPONSE"].fields_by_name["client_secret"]._options = None
    _globals["_CREATESERVICETOKENRESPONSE"].fields_by_name["client_secret"]._serialized_options = b"\330\241'\001"
    _globals["_UPDATESERVICETOKENREQUEST_FEATURETAGTOPERMISSIONENTRY"]._options = None
    _globals["_UPDATESERVICETOKENREQUEST_FEATURETAGTOPERMISSIONENTRY"]._serialized_options = b"8\001"
    _globals["_TEAMSERVICE"].methods_by_name["GetEnv"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name["GetEnv"]._serialized_options = b"\220\002\001\200}\013"
    _globals["_TEAMSERVICE"].methods_by_name["GetEnvironments"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name["GetEnvironments"]._serialized_options = b"\220\002\001\200}\002"
    _globals["_TEAMSERVICE"].methods_by_name["GetAgent"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name["GetAgent"]._serialized_options = b"\220\002\001\200}\002"
    _globals["_TEAMSERVICE"].methods_by_name["GetDisplayAgent"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name["GetDisplayAgent"]._serialized_options = b"\220\002\001\200}\002"
    _globals["_TEAMSERVICE"].methods_by_name["GetTeam"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name["GetTeam"]._serialized_options = b"\220\002\001\200}\002"
    _globals["_TEAMSERVICE"].methods_by_name["CreateTeam"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name["CreateTeam"]._serialized_options = b"\200}\033\212\323\016\002\010\002"
    _globals["_TEAMSERVICE"].methods_by_name["CreateProject"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name["CreateProject"]._serialized_options = b"\200}\032\212\323\016\002\010\002"
    _globals["_TEAMSERVICE"].methods_by_name["CreateEnvironment"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name[
        "CreateEnvironment"
    ]._serialized_options = b"\200}\032\212\323\016\002\010\002"
    _globals["_TEAMSERVICE"].methods_by_name["UpdateEnvironment"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name[
        "UpdateEnvironment"
    ]._serialized_options = b"\200}\014\212\323\016\002\010\002"
    _globals["_TEAMSERVICE"].methods_by_name["GetAvailablePermissions"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name["GetAvailablePermissions"]._serialized_options = b"\220\002\001\200}\002"
    _globals["_TEAMSERVICE"].methods_by_name["CreateServiceToken"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name[
        "CreateServiceToken"
    ]._serialized_options = b"\200}\025\212\323\016\031\010\002\022\025Created service token"
    _globals["_TEAMSERVICE"].methods_by_name["DeleteServiceToken"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name[
        "DeleteServiceToken"
    ]._serialized_options = b"\200}\025\212\323\016\002\010\002"
    _globals["_TEAMSERVICE"].methods_by_name["ListServiceTokens"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name["ListServiceTokens"]._serialized_options = b"\200}\026"
    _globals["_TEAMSERVICE"].methods_by_name["UpdateServiceToken"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name[
        "UpdateServiceToken"
    ]._serialized_options = b"\200}\025\212\323\016\002\010\002"
    _globals["_TEAMSERVICE"].methods_by_name["InviteTeamMember"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name[
        "InviteTeamMember"
    ]._serialized_options = b"\200}\007\212\323\016\002\010\002"
    _globals["_TEAMSERVICE"].methods_by_name["ExpireTeamInvite"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name[
        "ExpireTeamInvite"
    ]._serialized_options = b"\200}\010\212\323\016\002\010\002"
    _globals["_TEAMSERVICE"].methods_by_name["ListTeamInvites"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name["ListTeamInvites"]._serialized_options = b"\200}\t"
    _globals["_TEAMSERVICE"].methods_by_name["UpsertFeaturePermissions"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name[
        "UpsertFeaturePermissions"
    ]._serialized_options = b"\200}\025\212\323\016\002\010\002"
    _globals["_TEAMSERVICE"].methods_by_name["UpdateScimGroupSettings"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name[
        "UpdateScimGroupSettings"
    ]._serialized_options = b"\200}\n\212\323\016\002\010\002"
    _globals["_TEAMSERVICE"].methods_by_name["GetTeamPermissions"]._options = None
    _globals["_TEAMSERVICE"].methods_by_name["GetTeamPermissions"]._serialized_options = b"\200}\002"
    _globals["_GETENVREQUEST"]._serialized_start = 405
    _globals["_GETENVREQUEST"]._serialized_end = 420
    _globals["_GETENVRESPONSE"]._serialized_start = 422
    _globals["_GETENVRESPONSE"]._serialized_end = 502
    _globals["_GETENVIRONMENTSREQUEST"]._serialized_start = 504
    _globals["_GETENVIRONMENTSREQUEST"]._serialized_end = 554
    _globals["_GETENVIRONMENTSRESPONSE"]._serialized_start = 556
    _globals["_GETENVIRONMENTSRESPONSE"]._serialized_end = 647
    _globals["_GETAGENTREQUEST"]._serialized_start = 649
    _globals["_GETAGENTREQUEST"]._serialized_end = 666
    _globals["_GETAGENTRESPONSE"]._serialized_start = 668
    _globals["_GETAGENTRESPONSE"]._serialized_end = 730
    _globals["_GETDISPLAYAGENTREQUEST"]._serialized_start = 732
    _globals["_GETDISPLAYAGENTREQUEST"]._serialized_end = 756
    _globals["_GETDISPLAYAGENTRESPONSE"]._serialized_start = 758
    _globals["_GETDISPLAYAGENTRESPONSE"]._serialized_end = 834
    _globals["_TEAM"]._serialized_start = 837
    _globals["_TEAM"]._serialized_end = 1223
    _globals["_TEAM_SPECCONFIGJSONENTRY"]._serialized_start = 1107
    _globals["_TEAM_SPECCONFIGJSONENTRY"]._serialized_end = 1196
    _globals["_PROJECT"]._serialized_start = 1226
    _globals["_PROJECT"]._serialized_end = 1407
    _globals["_CREATETEAMREQUEST"]._serialized_start = 1409
    _globals["_CREATETEAMREQUEST"]._serialized_end = 1502
    _globals["_CREATETEAMRESPONSE"]._serialized_start = 1504
    _globals["_CREATETEAMRESPONSE"]._serialized_end = 1567
    _globals["_CREATEPROJECTREQUEST"]._serialized_start = 1569
    _globals["_CREATEPROJECTREQUEST"]._serialized_end = 1611
    _globals["_CREATEPROJECTRESPONSE"]._serialized_start = 1613
    _globals["_CREATEPROJECTRESPONSE"]._serialized_end = 1688
    _globals["_CREATEENVIRONMENTREQUEST"]._serialized_start = 1690
    _globals["_CREATEENVIRONMENTREQUEST"]._serialized_end = 1798
    _globals["_CREATEENVIRONMENTRESPONSE"]._serialized_start = 1800
    _globals["_CREATEENVIRONMENTRESPONSE"]._serialized_end = 1891
    _globals["_UPDATEENVIRONMENTOPERATION"]._serialized_start = 1894
    _globals["_UPDATEENVIRONMENTOPERATION"]._serialized_end = 2179
    _globals["_UPDATEENVIRONMENTOPERATION_ADDITIONALENVVARSENTRY"]._serialized_start = 2089
    _globals["_UPDATEENVIRONMENTOPERATION_ADDITIONALENVVARSENTRY"]._serialized_end = 2157
    _globals["_UPDATEENVIRONMENTREQUEST"]._serialized_start = 2182
    _globals["_UPDATEENVIRONMENTREQUEST"]._serialized_end = 2354
    _globals["_UPDATEENVIRONMENTRESPONSE"]._serialized_start = 2356
    _globals["_UPDATEENVIRONMENTRESPONSE"]._serialized_end = 2447
    _globals["_GETTEAMREQUEST"]._serialized_start = 2449
    _globals["_GETTEAMREQUEST"]._serialized_end = 2465
    _globals["_GETTEAMRESPONSE"]._serialized_start = 2467
    _globals["_GETTEAMRESPONSE"]._serialized_end = 2527
    _globals["_CREATESERVICETOKENREQUEST"]._serialized_start = 2530
    _globals["_CREATESERVICETOKENREQUEST"]._serialized_end = 2989
    _globals["_CREATESERVICETOKENREQUEST_FEATURETAGTOPERMISSIONENTRY"]._serialized_start = 2882
    _globals["_CREATESERVICETOKENREQUEST_FEATURETAGTOPERMISSIONENTRY"]._serialized_end = 2989
    _globals["_CREATESERVICETOKENRESPONSE"]._serialized_start = 2991
    _globals["_CREATESERVICETOKENRESPONSE"]._serialized_end = 3118
    _globals["_DELETESERVICETOKENREQUEST"]._serialized_start = 3120
    _globals["_DELETESERVICETOKENREQUEST"]._serialized_end = 3163
    _globals["_DELETESERVICETOKENRESPONSE"]._serialized_start = 3165
    _globals["_DELETESERVICETOKENRESPONSE"]._serialized_end = 3193
    _globals["_PERMISSIONDESCRIPTION"]._serialized_start = 3196
    _globals["_PERMISSIONDESCRIPTION"]._serialized_end = 3411
    _globals["_ROLEDESCRIPTION"]._serialized_start = 3414
    _globals["_ROLEDESCRIPTION"]._serialized_end = 3677
    _globals["_GETAVAILABLEPERMISSIONSREQUEST"]._serialized_start = 3679
    _globals["_GETAVAILABLEPERMISSIONSREQUEST"]._serialized_end = 3711
    _globals["_GETAVAILABLEPERMISSIONSRESPONSE"]._serialized_start = 3714
    _globals["_GETAVAILABLEPERMISSIONSRESPONSE"]._serialized_end = 3983
    _globals["_UPSERTFEATUREPERMISSIONSREQUEST"]._serialized_start = 3985
    _globals["_UPSERTFEATUREPERMISSIONSREQUEST"]._serialized_end = 4107
    _globals["_UPSERTFEATUREPERMISSIONSRESPONSE"]._serialized_start = 4109
    _globals["_UPSERTFEATUREPERMISSIONSRESPONSE"]._serialized_end = 4232
    _globals["_LISTSERVICETOKENSREQUEST"]._serialized_start = 4234
    _globals["_LISTSERVICETOKENSREQUEST"]._serialized_end = 4260
    _globals["_LISTSERVICETOKENSRESPONSE"]._serialized_start = 4262
    _globals["_LISTSERVICETOKENSRESPONSE"]._serialized_end = 4354
    _globals["_UPDATESERVICETOKENREQUEST"]._serialized_start = 4357
    _globals["_UPDATESERVICETOKENREQUEST"]._serialized_end = 4804
    _globals["_UPDATESERVICETOKENREQUEST_FEATURETAGTOPERMISSIONENTRY"]._serialized_start = 2882
    _globals["_UPDATESERVICETOKENREQUEST_FEATURETAGTOPERMISSIONENTRY"]._serialized_end = 2989
    _globals["_UPDATESERVICETOKENRESPONSE"]._serialized_start = 4806
    _globals["_UPDATESERVICETOKENRESPONSE"]._serialized_end = 4897
    _globals["_UPDATESCIMGROUPSETTINGSREQUEST"]._serialized_start = 4899
    _globals["_UPDATESCIMGROUPSETTINGSREQUEST"]._serialized_end = 4984
    _globals["_UPDATESCIMGROUPSETTINGSRESPONSE"]._serialized_start = 4986
    _globals["_UPDATESCIMGROUPSETTINGSRESPONSE"]._serialized_end = 5050
    _globals["_INVITETEAMMEMBERREQUEST"]._serialized_start = 5052
    _globals["_INVITETEAMMEMBERREQUEST"]._serialized_end = 5141
    _globals["_INVITETEAMMEMBERRESPONSE"]._serialized_start = 5143
    _globals["_INVITETEAMMEMBERRESPONSE"]._serialized_end = 5169
    _globals["_EXPIRETEAMINVITEREQUEST"]._serialized_start = 5171
    _globals["_EXPIRETEAMINVITEREQUEST"]._serialized_end = 5212
    _globals["_EXPIRETEAMINVITERESPONSE"]._serialized_start = 5214
    _globals["_EXPIRETEAMINVITERESPONSE"]._serialized_end = 5240
    _globals["_TEAMINVITE"]._serialized_start = 5243
    _globals["_TEAMINVITE"]._serialized_end = 5406
    _globals["_LISTTEAMINVITESREQUEST"]._serialized_start = 5408
    _globals["_LISTTEAMINVITESREQUEST"]._serialized_end = 5432
    _globals["_LISTTEAMINVITESRESPONSE"]._serialized_start = 5434
    _globals["_LISTTEAMINVITESRESPONSE"]._serialized_end = 5514
    _globals["_SCIMGROUP"]._serialized_start = 5516
    _globals["_SCIMGROUP"]._serialized_end = 5620
    _globals["_SCIMGROUPROLEASSIGNMENT"]._serialized_start = 5623
    _globals["_SCIMGROUPROLEASSIGNMENT"]._serialized_end = 5770
    _globals["_USERROLEASSIGNMENT"]._serialized_start = 5772
    _globals["_USERROLEASSIGNMENT"]._serialized_end = 5837
    _globals["_USERPERMISSIONS"]._serialized_start = 5840
    _globals["_USERPERMISSIONS"]._serialized_end = 6059
    _globals["_USER"]._serialized_start = 6062
    _globals["_USER"]._serialized_end = 6325
    _globals["_ENVIRONMENTPERMISSIONS"]._serialized_start = 6328
    _globals["_ENVIRONMENTPERMISSIONS"]._serialized_end = 6541
    _globals["_GETTEAMPERMISSIONSREQUEST"]._serialized_start = 6543
    _globals["_GETTEAMPERMISSIONSREQUEST"]._serialized_end = 6570
    _globals["_GETTEAMPERMISSIONSRESPONSE"]._serialized_start = 6573
    _globals["_GETTEAMPERMISSIONSRESPONSE"]._serialized_end = 6874
    _globals["_TEAMSERVICE"]._serialized_start = 6877
    _globals["_TEAMSERVICE"]._serialized_end = 9183
# @@protoc_insertion_point(module_scope)
