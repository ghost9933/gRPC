/* This file was generated by upb_generator from the input file:
 *
 *     envoy/config/trace/v3/datadog.proto
 *
 * Do not edit -- your changes will be discarded when the file is
 * regenerated. */

#include <stddef.h>
#include "upb/generated_code_support.h"
#include "envoy/config/trace/v3/datadog.upb_minitable.h"
#include "google/protobuf/duration.upb_minitable.h"
#include "udpa/annotations/migrate.upb_minitable.h"
#include "udpa/annotations/status.upb_minitable.h"
#include "udpa/annotations/versioning.upb_minitable.h"
#include "validate/validate.upb_minitable.h"

// Must be last.
#include "upb/port/def.inc"

static const upb_MiniTableSub envoy_config_trace_v3_DatadogRemoteConfig_submsgs[1] = {
  {.UPB_PRIVATE(submsg) = &google__protobuf__Duration_msg_init},
};

static const upb_MiniTableField envoy_config_trace_v3_DatadogRemoteConfig__fields[1] = {
  {1, UPB_SIZE(12, 16), 64, 0, 11, (int)kUpb_FieldMode_Scalar | ((int)UPB_SIZE(kUpb_FieldRep_4Byte, kUpb_FieldRep_8Byte) << kUpb_FieldRep_Shift)},
};

const upb_MiniTable envoy__config__trace__v3__DatadogRemoteConfig_msg_init = {
  &envoy_config_trace_v3_DatadogRemoteConfig_submsgs[0],
  &envoy_config_trace_v3_DatadogRemoteConfig__fields[0],
  UPB_SIZE(16, 24), 1, kUpb_ExtMode_NonExtendable, 1, UPB_FASTTABLE_MASK(255), 0,
#ifdef UPB_TRACING_ENABLED
  "envoy.config.trace.v3.DatadogRemoteConfig",
#endif
};

static const upb_MiniTableSub envoy_config_trace_v3_DatadogConfig_submsgs[1] = {
  {.UPB_PRIVATE(submsg) = &envoy__config__trace__v3__DatadogRemoteConfig_msg_init},
};

static const upb_MiniTableField envoy_config_trace_v3_DatadogConfig__fields[4] = {
  {1, 16, 0, kUpb_NoSub, 9, (int)kUpb_FieldMode_Scalar | ((int)kUpb_FieldRep_StringView << kUpb_FieldRep_Shift)},
  {2, UPB_SIZE(24, 32), 0, kUpb_NoSub, 9, (int)kUpb_FieldMode_Scalar | ((int)kUpb_FieldRep_StringView << kUpb_FieldRep_Shift)},
  {3, UPB_SIZE(32, 48), 0, kUpb_NoSub, 9, (int)kUpb_FieldMode_Scalar | ((int)kUpb_FieldRep_StringView << kUpb_FieldRep_Shift)},
  {4, UPB_SIZE(12, 64), 64, 0, 11, (int)kUpb_FieldMode_Scalar | ((int)UPB_SIZE(kUpb_FieldRep_4Byte, kUpb_FieldRep_8Byte) << kUpb_FieldRep_Shift)},
};

const upb_MiniTable envoy__config__trace__v3__DatadogConfig_msg_init = {
  &envoy_config_trace_v3_DatadogConfig_submsgs[0],
  &envoy_config_trace_v3_DatadogConfig__fields[0],
  UPB_SIZE(40, 72), 4, kUpb_ExtMode_NonExtendable, 4, UPB_FASTTABLE_MASK(24), 0,
#ifdef UPB_TRACING_ENABLED
  "envoy.config.trace.v3.DatadogConfig",
#endif
  UPB_FASTTABLE_INIT({
    {0x0000000000000000, &_upb_FastDecoder_DecodeGeneric},
    {0x001000003f00000a, &upb_pss_1bt},
    {0x002000003f000012, &upb_pss_1bt},
    {0x003000003f00001a, &upb_pss_1bt},
  })
};

static const upb_MiniTable *messages_layout[2] = {
  &envoy__config__trace__v3__DatadogRemoteConfig_msg_init,
  &envoy__config__trace__v3__DatadogConfig_msg_init,
};

const upb_MiniTableFile envoy_config_trace_v3_datadog_proto_upb_file_layout = {
  messages_layout,
  NULL,
  NULL,
  2,
  0,
  0,
};

#include "upb/port/undef.inc"
