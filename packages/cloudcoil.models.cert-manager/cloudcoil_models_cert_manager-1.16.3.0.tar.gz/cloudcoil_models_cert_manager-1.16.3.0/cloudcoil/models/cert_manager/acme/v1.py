from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Dict, List, Literal, Optional

from pydantic import Field

from cloudcoil import apimachinery
from cloudcoil.pydantic import BaseModel
from cloudcoil.resources import Resource


class IssuerRef(BaseModel):
    group: Annotated[
        Optional[str], Field(description="Group of the resource being referred to.")
    ] = None
    kind: Annotated[Optional[str], Field(description="Kind of the resource being referred to.")] = (
        None
    )
    name: Annotated[str, Field(description="Name of the resource being referred to.")]


class AcmeDns(BaseModel):
    account_secret_ref: Annotated[
        SecretRef,
        Field(
            alias="accountSecretRef",
            description="A reference to a specific 'key' within a Secret resource.\nIn some instances, `key` is a required field.",
        ),
    ]
    host: str


class Akamai(BaseModel):
    access_token_secret_ref: Annotated[
        SecretRef,
        Field(
            alias="accessTokenSecretRef",
            description="A reference to a specific 'key' within a Secret resource.\nIn some instances, `key` is a required field.",
        ),
    ]
    client_secret_secret_ref: Annotated[
        SecretRef,
        Field(
            alias="clientSecretSecretRef",
            description="A reference to a specific 'key' within a Secret resource.\nIn some instances, `key` is a required field.",
        ),
    ]
    client_token_secret_ref: Annotated[
        SecretRef,
        Field(
            alias="clientTokenSecretRef",
            description="A reference to a specific 'key' within a Secret resource.\nIn some instances, `key` is a required field.",
        ),
    ]
    service_consumer_domain: Annotated[str, Field(alias="serviceConsumerDomain")]


class ManagedIdentity(BaseModel):
    client_id: Annotated[
        Optional[str],
        Field(
            alias="clientID",
            description="client ID of the managed identity, can not be used at the same time as resourceID",
        ),
    ] = None
    resource_id: Annotated[
        Optional[str],
        Field(
            alias="resourceID",
            description="resource ID of the managed identity, can not be used at the same time as clientID\nCannot be used for Azure Managed Service Identity",
        ),
    ] = None


class AzureDns(BaseModel):
    client_id: Annotated[
        Optional[str],
        Field(
            alias="clientID",
            description="Auth: Azure Service Principal:\nThe ClientID of the Azure Service Principal used to authenticate with Azure DNS.\nIf set, ClientSecret and TenantID must also be set.",
        ),
    ] = None
    client_secret_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="clientSecretSecretRef",
            description="Auth: Azure Service Principal:\nA reference to a Secret containing the password associated with the Service Principal.\nIf set, ClientID and TenantID must also be set.",
        ),
    ] = None
    environment: Annotated[
        Optional[
            Literal[
                "AzurePublicCloud", "AzureChinaCloud", "AzureGermanCloud", "AzureUSGovernmentCloud"
            ]
        ],
        Field(description="name of the Azure environment (default AzurePublicCloud)"),
    ] = None
    hosted_zone_name: Annotated[
        Optional[str],
        Field(alias="hostedZoneName", description="name of the DNS zone that should be used"),
    ] = None
    managed_identity: Annotated[
        Optional[ManagedIdentity],
        Field(
            alias="managedIdentity",
            description="Auth: Azure Workload Identity or Azure Managed Service Identity:\nSettings to enable Azure Workload Identity or Azure Managed Service Identity\nIf set, ClientID, ClientSecret and TenantID must not be set.",
        ),
    ] = None
    resource_group_name: Annotated[
        str,
        Field(alias="resourceGroupName", description="resource group the DNS zone is located in"),
    ]
    subscription_id: Annotated[
        str, Field(alias="subscriptionID", description="ID of the Azure subscription")
    ]
    tenant_id: Annotated[
        Optional[str],
        Field(
            alias="tenantID",
            description="Auth: Azure Service Principal:\nThe TenantID of the Azure Service Principal used to authenticate with Azure DNS.\nIf set, ClientID and ClientSecret must also be set.",
        ),
    ] = None


class CloudDns(BaseModel):
    hosted_zone_name: Annotated[
        Optional[str],
        Field(
            alias="hostedZoneName",
            description="HostedZoneName is an optional field that tells cert-manager in which\nCloud DNS zone the challenge record has to be created.\nIf left empty cert-manager will automatically choose a zone.",
        ),
    ] = None
    project: str
    service_account_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="serviceAccountSecretRef",
            description="A reference to a specific 'key' within a Secret resource.\nIn some instances, `key` is a required field.",
        ),
    ] = None


class Cloudflare(BaseModel):
    api_key_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="apiKeySecretRef",
            description="API key to use to authenticate with Cloudflare.\nNote: using an API token to authenticate is now the recommended method\nas it allows greater control of permissions.",
        ),
    ] = None
    api_token_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="apiTokenSecretRef", description="API token used to authenticate with Cloudflare."
        ),
    ] = None
    email: Annotated[
        Optional[str],
        Field(
            description="Email of the account, only required when using API key based authentication."
        ),
    ] = None


class Digitalocean(BaseModel):
    token_secret_ref: Annotated[
        SecretRef,
        Field(
            alias="tokenSecretRef",
            description="A reference to a specific 'key' within a Secret resource.\nIn some instances, `key` is a required field.",
        ),
    ]


class Rfc2136(BaseModel):
    nameserver: Annotated[
        str,
        Field(
            description="The IP address or hostname of an authoritative DNS server supporting\nRFC2136 in the form host:port. If the host is an IPv6 address it must be\nenclosed in square brackets (e.g [2001:db8::1])\xa0; port is optional.\nThis field is required."
        ),
    ]
    tsig_algorithm: Annotated[
        Optional[str],
        Field(
            alias="tsigAlgorithm",
            description="The TSIG Algorithm configured in the DNS supporting RFC2136. Used only\nwhen ``tsigSecretSecretRef`` and ``tsigKeyName`` are defined.\nSupported values are (case-insensitive): ``HMACMD5`` (default),\n``HMACSHA1``, ``HMACSHA256`` or ``HMACSHA512``.",
        ),
    ] = None
    tsig_key_name: Annotated[
        Optional[str],
        Field(
            alias="tsigKeyName",
            description="The TSIG Key name configured in the DNS.\nIf ``tsigSecretSecretRef`` is defined, this field is required.",
        ),
    ] = None
    tsig_secret_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="tsigSecretSecretRef",
            description="The name of the secret containing the TSIG value.\nIf ``tsigKeyName`` is defined, this field is required.",
        ),
    ] = None


class SecretRef(BaseModel):
    key: Annotated[
        Optional[str],
        Field(
            description="The key of the entry in the Secret resource's `data` field to be used.\nSome instances of this field may be defaulted, in others it may be\nrequired."
        ),
    ] = None
    name: Annotated[
        str,
        Field(
            description="Name of the resource being referred to.\nMore info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    ]


class ServiceAccountRef(BaseModel):
    audiences: Annotated[
        Optional[List[str]],
        Field(
            description="TokenAudiences is an optional list of audiences to include in the\ntoken passed to AWS. The default token consisting of the issuer's namespace\nand name is always included.\nIf unset the audience defaults to `sts.amazonaws.com`."
        ),
    ] = None
    name: Annotated[str, Field(description="Name of the ServiceAccount used to request a token.")]


class KubernetesRoute53Auth(BaseModel):
    service_account_ref: Annotated[
        ServiceAccountRef,
        Field(
            alias="serviceAccountRef",
            description='A reference to a service account that will be used to request a bound\ntoken (also known as "projected token"). To use this field, you must\nconfigure an RBAC rule to let cert-manager request a token.',
        ),
    ]


class Route53Auth(BaseModel):
    kubernetes: Annotated[
        KubernetesRoute53Auth,
        Field(
            description="Kubernetes authenticates with Route53 using AssumeRoleWithWebIdentity\nby passing a bound ServiceAccount token."
        ),
    ]


class Route53(BaseModel):
    access_key_id: Annotated[
        Optional[str],
        Field(
            alias="accessKeyID",
            description="The AccessKeyID is used for authentication.\nCannot be set when SecretAccessKeyID is set.\nIf neither the Access Key nor Key ID are set, we fall-back to using env\nvars, shared credentials file or AWS Instance metadata,\nsee: https://docs.aws.amazon.com/sdk-for-go/v1/developer-guide/configuring-sdk.html#specifying-credentials",
        ),
    ] = None
    access_key_id_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="accessKeyIDSecretRef",
            description="The SecretAccessKey is used for authentication. If set, pull the AWS\naccess key ID from a key within a Kubernetes Secret.\nCannot be set when AccessKeyID is set.\nIf neither the Access Key nor Key ID are set, we fall-back to using env\nvars, shared credentials file or AWS Instance metadata,\nsee: https://docs.aws.amazon.com/sdk-for-go/v1/developer-guide/configuring-sdk.html#specifying-credentials",
        ),
    ] = None
    auth: Annotated[
        Optional[Route53Auth], Field(description="Auth configures how cert-manager authenticates.")
    ] = None
    hosted_zone_id: Annotated[
        Optional[str],
        Field(
            alias="hostedZoneID",
            description="If set, the provider will manage only this zone in Route53 and will not do a lookup using the route53:ListHostedZonesByName api call.",
        ),
    ] = None
    region: Annotated[
        Optional[str],
        Field(
            description="Override the AWS region.\n\nRoute53 is a global service and does not have regional endpoints but the\nregion specified here (or via environment variables) is used as a hint to\nhelp compute the correct AWS credential scope and partition when it\nconnects to Route53. See:\n- [Amazon Route 53 endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/r53.html)\n- [Global services](https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/global-services.html)\n\nIf you omit this region field, cert-manager will use the region from\nAWS_REGION and AWS_DEFAULT_REGION environment variables, if they are set\nin the cert-manager controller Pod.\n\nThe `region` field is not needed if you use [IAM Roles for Service Accounts (IRSA)](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html).\nInstead an AWS_REGION environment variable is added to the cert-manager controller Pod by:\n[Amazon EKS Pod Identity Webhook](https://github.com/aws/amazon-eks-pod-identity-webhook).\nIn this case this `region` field value is ignored.\n\nThe `region` field is not needed if you use [EKS Pod Identities](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html).\nInstead an AWS_REGION environment variable is added to the cert-manager controller Pod by:\n[Amazon EKS Pod Identity Agent](https://github.com/aws/eks-pod-identity-agent),\nIn this case this `region` field value is ignored."
        ),
    ] = None
    role: Annotated[
        Optional[str],
        Field(
            description="Role is a Role ARN which the Route53 provider will assume using either the explicit credentials AccessKeyID/SecretAccessKey\nor the inferred credentials from environment variables, shared credentials file or AWS Instance metadata"
        ),
    ] = None
    secret_access_key_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="secretAccessKeySecretRef",
            description="The SecretAccessKey is used for authentication.\nIf neither the Access Key nor Key ID are set, we fall-back to using env\nvars, shared credentials file or AWS Instance metadata,\nsee: https://docs.aws.amazon.com/sdk-for-go/v1/developer-guide/configuring-sdk.html#specifying-credentials",
        ),
    ] = None


class Webhook(BaseModel):
    config: Annotated[
        Optional[Any],
        Field(
            description="Additional configuration that should be passed to the webhook apiserver\nwhen challenges are processed.\nThis can contain arbitrary JSON data.\nSecret values should not be specified in this stanza.\nIf secret values are needed (e.g. credentials for a DNS service), you\nshould use a SecretKeySelector to reference a Secret resource.\nFor details on the schema of this field, consult the webhook provider\nimplementation's documentation."
        ),
    ] = None
    group_name: Annotated[
        str,
        Field(
            alias="groupName",
            description="The API group name that should be used when POSTing ChallengePayload\nresources to the webhook apiserver.\nThis should be the same as the GroupName specified in the webhook\nprovider implementation.",
        ),
    ]
    solver_name: Annotated[
        str,
        Field(
            alias="solverName",
            description="The name of the solver to use, as defined in the webhook provider\nimplementation.\nThis will typically be the name of the provider, e.g. 'cloudflare'.",
        ),
    ]


class Dns01(BaseModel):
    acme_dns: Annotated[
        Optional[AcmeDns],
        Field(
            alias="acmeDNS",
            description="Use the 'ACME DNS' (https://github.com/joohoi/acme-dns) API to manage\nDNS01 challenge records.",
        ),
    ] = None
    akamai: Annotated[
        Optional[Akamai],
        Field(
            description="Use the Akamai DNS zone management API to manage DNS01 challenge records."
        ),
    ] = None
    azure_dns: Annotated[
        Optional[AzureDns],
        Field(
            alias="azureDNS",
            description="Use the Microsoft Azure DNS API to manage DNS01 challenge records.",
        ),
    ] = None
    cloud_dns: Annotated[
        Optional[CloudDns],
        Field(
            alias="cloudDNS",
            description="Use the Google Cloud DNS API to manage DNS01 challenge records.",
        ),
    ] = None
    cloudflare: Annotated[
        Optional[Cloudflare],
        Field(description="Use the Cloudflare API to manage DNS01 challenge records."),
    ] = None
    cname_strategy: Annotated[
        Optional[Literal["None", "Follow"]],
        Field(
            alias="cnameStrategy",
            description="CNAMEStrategy configures how the DNS01 provider should handle CNAME\nrecords when found in DNS zones.",
        ),
    ] = None
    digitalocean: Annotated[
        Optional[Digitalocean],
        Field(description="Use the DigitalOcean DNS API to manage DNS01 challenge records."),
    ] = None
    rfc2136: Annotated[
        Optional[Rfc2136],
        Field(
            description='Use RFC2136 ("Dynamic Updates in the Domain Name System") (https://datatracker.ietf.org/doc/rfc2136/)\nto manage DNS01 challenge records.'
        ),
    ] = None
    route53: Annotated[
        Optional[Route53],
        Field(description="Use the AWS Route53 API to manage DNS01 challenge records."),
    ] = None
    webhook: Annotated[
        Optional[Webhook],
        Field(
            description="Configure an external webhook based DNS01 challenge solver to manage\nDNS01 challenge records."
        ),
    ] = None


class ParentRef(BaseModel):
    group: Annotated[
        Optional[str],
        Field(
            description='Group is the group of the referent.\nWhen unspecified, "gateway.networking.k8s.io" is inferred.\nTo set the core API group (such as for a "Service" kind referent),\nGroup must be explicitly set to "" (empty string).\n\nSupport: Core',
            max_length=253,
            pattern="^$|^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$",
        ),
    ] = "gateway.networking.k8s.io"
    kind: Annotated[
        Optional[str],
        Field(
            description='Kind is kind of the referent.\n\nThere are two kinds of parent resources with "Core" support:\n\n* Gateway (Gateway conformance profile)\n* Service (Mesh conformance profile, ClusterIP Services only)\n\nSupport for other resources is Implementation-Specific.',
            max_length=63,
            min_length=1,
            pattern="^[a-zA-Z]([-a-zA-Z0-9]*[a-zA-Z0-9])?$",
        ),
    ] = "Gateway"
    name: Annotated[
        str,
        Field(
            description="Name is the name of the referent.\n\nSupport: Core",
            max_length=253,
            min_length=1,
        ),
    ]
    namespace: Annotated[
        Optional[str],
        Field(
            description='Namespace is the namespace of the referent. When unspecified, this refers\nto the local namespace of the Route.\n\nNote that there are specific rules for ParentRefs which cross namespace\nboundaries. Cross-namespace references are only valid if they are explicitly\nallowed by something in the namespace they are referring to. For example:\nGateway has the AllowedRoutes field, and ReferenceGrant provides a\ngeneric way to enable any other kind of cross-namespace reference.\n\n<gateway:experimental:description>\nParentRefs from a Route to a Service in the same namespace are "producer"\nroutes, which apply default routing rules to inbound connections from\nany namespace to the Service.\n\nParentRefs from a Route to a Service in a different namespace are\n"consumer" routes, and these routing rules are only applied to outbound\nconnections originating from the same namespace as the Route, for which\nthe intended destination of the connections are a Service targeted as a\nParentRef of the Route.\n</gateway:experimental:description>\n\nSupport: Core',
            max_length=63,
            min_length=1,
            pattern="^[a-z0-9]([-a-z0-9]*[a-z0-9])?$",
        ),
    ] = None
    port: Annotated[
        Optional[int],
        Field(
            description="Port is the network port this Route targets. It can be interpreted\ndifferently based on the type of parent resource.\n\nWhen the parent resource is a Gateway, this targets all listeners\nlistening on the specified port that also support this kind of Route(and\nselect this Route). It's not recommended to set `Port` unless the\nnetworking behaviors specified in a Route must apply to a specific port\nas opposed to a listener(s) whose port(s) may be changed. When both Port\nand SectionName are specified, the name and port of the selected listener\nmust match both specified values.\n\n<gateway:experimental:description>\nWhen the parent resource is a Service, this targets a specific port in the\nService spec. When both Port (experimental) and SectionName are specified,\nthe name and port of the selected port must match both specified values.\n</gateway:experimental:description>\n\nImplementations MAY choose to support other parent resources.\nImplementations supporting other types of parent resources MUST clearly\ndocument how/if Port is interpreted.\n\nFor the purpose of status, an attachment is considered successful as\nlong as the parent resource accepts it partially. For example, Gateway\nlisteners can restrict which Routes can attach to them by Route kind,\nnamespace, or hostname. If 1 of 2 Gateway listeners accept attachment\nfrom the referencing Route, the Route MUST be considered successfully\nattached. If no Gateway listeners accept attachment from this Route,\nthe Route MUST be considered detached from the Gateway.\n\nSupport: Extended",
            ge=1,
            le=65535,
        ),
    ] = None
    section_name: Annotated[
        Optional[str],
        Field(
            alias="sectionName",
            description="SectionName is the name of a section within the target resource. In the\nfollowing resources, SectionName is interpreted as the following:\n\n* Gateway: Listener name. When both Port (experimental) and SectionName\nare specified, the name and port of the selected listener must match\nboth specified values.\n* Service: Port name. When both Port (experimental) and SectionName\nare specified, the name and port of the selected listener must match\nboth specified values.\n\nImplementations MAY choose to support attaching Routes to other resources.\nIf that is the case, they MUST clearly document how SectionName is\ninterpreted.\n\nWhen unspecified (empty string), this will reference the entire resource.\nFor the purpose of status, an attachment is considered successful if at\nleast one section in the parent resource accepts it. For example, Gateway\nlisteners can restrict which Routes can attach to them by Route kind,\nnamespace, or hostname. If 1 of 2 Gateway listeners accept attachment from\nthe referencing Route, the Route MUST be considered successfully\nattached. If no Gateway listeners accept attachment from this Route, the\nRoute MUST be considered detached from the Gateway.\n\nSupport: Core",
            max_length=253,
            min_length=1,
            pattern="^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$",
        ),
    ] = None


class Metadata(BaseModel):
    annotations: Annotated[
        Optional[Dict[str, str]],
        Field(
            description="Annotations that should be added to the created ACME HTTP01 solver pods."
        ),
    ] = None
    labels: Annotated[
        Optional[Dict[str, str]],
        Field(description="Labels that should be added to the created ACME HTTP01 solver pods."),
    ] = None


class MatchExpression(BaseModel):
    key: Annotated[str, Field(description="The label key that the selector applies to.")]
    operator: Annotated[
        str,
        Field(
            description="Represents a key's relationship to a set of values.\nValid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt."
        ),
    ]
    values: Annotated[
        Optional[List[str]],
        Field(
            description="An array of string values. If the operator is In or NotIn,\nthe values array must be non-empty. If the operator is Exists or DoesNotExist,\nthe values array must be empty. If the operator is Gt or Lt, the values\narray must have a single element, which will be interpreted as an integer.\nThis array is replaced during a strategic merge patch."
        ),
    ] = None


class PreferredDuringSchedulingIgnoredDuringExecution(BaseModel):
    preference: Annotated[
        NodeSelectorTerm,
        Field(description="A node selector term, associated with the corresponding weight."),
    ]
    weight: Annotated[
        int,
        Field(
            description="Weight associated with matching the corresponding nodeSelectorTerm, in the range 1-100."
        ),
    ]


class NodeSelectorTerm(BaseModel):
    match_expressions: Annotated[
        Optional[List[MatchExpression]],
        Field(
            alias="matchExpressions",
            description="A list of node selector requirements by node's labels.",
        ),
    ] = None
    match_fields: Annotated[
        Optional[List[MatchExpression]],
        Field(
            alias="matchFields",
            description="A list of node selector requirements by node's fields.",
        ),
    ] = None


class RequiredDuringSchedulingIgnoredDuringExecution(BaseModel):
    node_selector_terms: Annotated[
        List[NodeSelectorTerm],
        Field(
            alias="nodeSelectorTerms",
            description="Required. A list of node selector terms. The terms are ORed.",
        ),
    ]


class NodeAffinity(BaseModel):
    preferred_during_scheduling_ignored_during_execution: Annotated[
        Optional[List[PreferredDuringSchedulingIgnoredDuringExecution]],
        Field(
            alias="preferredDuringSchedulingIgnoredDuringExecution",
            description='The scheduler will prefer to schedule pods to nodes that satisfy\nthe affinity expressions specified by this field, but it may choose\na node that violates one or more of the expressions. The node that is\nmost preferred is the one with the greatest sum of weights, i.e.\nfor each node that meets all of the scheduling requirements (resource\nrequest, requiredDuringScheduling affinity expressions, etc.),\ncompute a sum by iterating through the elements of this field and adding\n"weight" to the sum if the node matches the corresponding matchExpressions; the\nnode(s) with the highest sum are the most preferred.',
        ),
    ] = None
    required_during_scheduling_ignored_during_execution: Annotated[
        Optional[RequiredDuringSchedulingIgnoredDuringExecution],
        Field(
            alias="requiredDuringSchedulingIgnoredDuringExecution",
            description="If the affinity requirements specified by this field are not met at\nscheduling time, the pod will not be scheduled onto the node.\nIf the affinity requirements specified by this field cease to be met\nat some point during pod execution (e.g. due to an update), the system\nmay or may not try to eventually evict the pod from its node.",
        ),
    ] = None


class MatchExpressionModel(BaseModel):
    key: Annotated[str, Field(description="key is the label key that the selector applies to.")]
    operator: Annotated[
        str,
        Field(
            description="operator represents a key's relationship to a set of values.\nValid operators are In, NotIn, Exists and DoesNotExist."
        ),
    ]
    values: Annotated[
        Optional[List[str]],
        Field(
            description="values is an array of string values. If the operator is In or NotIn,\nthe values array must be non-empty. If the operator is Exists or DoesNotExist,\nthe values array must be empty. This array is replaced during a strategic\nmerge patch."
        ),
    ] = None


class LabelSelector(BaseModel):
    match_expressions: Annotated[
        Optional[List[MatchExpressionModel]],
        Field(
            alias="matchExpressions",
            description="matchExpressions is a list of label selector requirements. The requirements are ANDed.",
        ),
    ] = None
    match_labels: Annotated[
        Optional[Dict[str, str]],
        Field(
            alias="matchLabels",
            description='matchLabels is a map of {key,value} pairs. A single {key,value} in the matchLabels\nmap is equivalent to an element of matchExpressions, whose key field is "key", the\noperator is "In", and the values array contains only "value". The requirements are ANDed.',
        ),
    ] = None


class PodAffinityTerm(BaseModel):
    label_selector: Annotated[
        Optional[LabelSelector],
        Field(
            alias="labelSelector",
            description="A label query over a set of resources, in this case pods.\nIf it's null, this PodAffinityTerm matches with no Pods.",
        ),
    ] = None
    match_label_keys: Annotated[
        Optional[List[str]],
        Field(
            alias="matchLabelKeys",
            description="MatchLabelKeys is a set of pod label keys to select which pods will\nbe taken into consideration. The keys are used to lookup values from the\nincoming pod labels, those key-value labels are merged with `labelSelector` as `key in (value)`\nto select the group of existing pods which pods will be taken into consideration\nfor the incoming pod's pod (anti) affinity. Keys that don't exist in the incoming\npod labels will be ignored. The default value is empty.\nThe same key is forbidden to exist in both matchLabelKeys and labelSelector.\nAlso, matchLabelKeys cannot be set when labelSelector isn't set.\nThis is a beta field and requires enabling MatchLabelKeysInPodAffinity feature gate (enabled by default).",
        ),
    ] = None
    mismatch_label_keys: Annotated[
        Optional[List[str]],
        Field(
            alias="mismatchLabelKeys",
            description="MismatchLabelKeys is a set of pod label keys to select which pods will\nbe taken into consideration. The keys are used to lookup values from the\nincoming pod labels, those key-value labels are merged with `labelSelector` as `key notin (value)`\nto select the group of existing pods which pods will be taken into consideration\nfor the incoming pod's pod (anti) affinity. Keys that don't exist in the incoming\npod labels will be ignored. The default value is empty.\nThe same key is forbidden to exist in both mismatchLabelKeys and labelSelector.\nAlso, mismatchLabelKeys cannot be set when labelSelector isn't set.\nThis is a beta field and requires enabling MatchLabelKeysInPodAffinity feature gate (enabled by default).",
        ),
    ] = None
    namespace_selector: Annotated[
        Optional[LabelSelector],
        Field(
            alias="namespaceSelector",
            description='A label query over the set of namespaces that the term applies to.\nThe term is applied to the union of the namespaces selected by this field\nand the ones listed in the namespaces field.\nnull selector and null or empty namespaces list means "this pod\'s namespace".\nAn empty selector ({}) matches all namespaces.',
        ),
    ] = None
    namespaces: Annotated[
        Optional[List[str]],
        Field(
            description='namespaces specifies a static list of namespace names that the term applies to.\nThe term is applied to the union of the namespaces listed in this field\nand the ones selected by namespaceSelector.\nnull or empty namespaces list and null namespaceSelector means "this pod\'s namespace".'
        ),
    ] = None
    topology_key: Annotated[
        str,
        Field(
            alias="topologyKey",
            description="This pod should be co-located (affinity) or not co-located (anti-affinity) with the pods matching\nthe labelSelector in the specified namespaces, where co-located is defined as running on a node\nwhose value of the label with key topologyKey matches that of any node on which any of the\nselected pods is running.\nEmpty topologyKey is not allowed.",
        ),
    ]


class PreferredDuringSchedulingIgnoredDuringExecutionModel(BaseModel):
    pod_affinity_term: Annotated[
        PodAffinityTerm,
        Field(
            alias="podAffinityTerm",
            description="Required. A pod affinity term, associated with the corresponding weight.",
        ),
    ]
    weight: Annotated[
        int,
        Field(
            description="weight associated with matching the corresponding podAffinityTerm,\nin the range 1-100."
        ),
    ]


class PodAffinity(BaseModel):
    preferred_during_scheduling_ignored_during_execution: Annotated[
        Optional[List[PreferredDuringSchedulingIgnoredDuringExecutionModel]],
        Field(
            alias="preferredDuringSchedulingIgnoredDuringExecution",
            description='The scheduler will prefer to schedule pods to nodes that satisfy\nthe affinity expressions specified by this field, but it may choose\na node that violates one or more of the expressions. The node that is\nmost preferred is the one with the greatest sum of weights, i.e.\nfor each node that meets all of the scheduling requirements (resource\nrequest, requiredDuringScheduling affinity expressions, etc.),\ncompute a sum by iterating through the elements of this field and adding\n"weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the\nnode(s) with the highest sum are the most preferred.',
        ),
    ] = None
    required_during_scheduling_ignored_during_execution: Annotated[
        Optional[List[PodAffinityTerm]],
        Field(
            alias="requiredDuringSchedulingIgnoredDuringExecution",
            description="If the affinity requirements specified by this field are not met at\nscheduling time, the pod will not be scheduled onto the node.\nIf the affinity requirements specified by this field cease to be met\nat some point during pod execution (e.g. due to a pod label update), the\nsystem may or may not try to eventually evict the pod from its node.\nWhen there are multiple elements, the lists of nodes corresponding to each\npodAffinityTerm are intersected, i.e. all terms must be satisfied.",
        ),
    ] = None


class PodAntiAffinity(BaseModel):
    preferred_during_scheduling_ignored_during_execution: Annotated[
        Optional[List[PreferredDuringSchedulingIgnoredDuringExecutionModel]],
        Field(
            alias="preferredDuringSchedulingIgnoredDuringExecution",
            description='The scheduler will prefer to schedule pods to nodes that satisfy\nthe anti-affinity expressions specified by this field, but it may choose\na node that violates one or more of the expressions. The node that is\nmost preferred is the one with the greatest sum of weights, i.e.\nfor each node that meets all of the scheduling requirements (resource\nrequest, requiredDuringScheduling anti-affinity expressions, etc.),\ncompute a sum by iterating through the elements of this field and adding\n"weight" to the sum if the node has pods which matches the corresponding podAffinityTerm; the\nnode(s) with the highest sum are the most preferred.',
        ),
    ] = None
    required_during_scheduling_ignored_during_execution: Annotated[
        Optional[List[PodAffinityTerm]],
        Field(
            alias="requiredDuringSchedulingIgnoredDuringExecution",
            description="If the anti-affinity requirements specified by this field are not met at\nscheduling time, the pod will not be scheduled onto the node.\nIf the anti-affinity requirements specified by this field cease to be met\nat some point during pod execution (e.g. due to a pod label update), the\nsystem may or may not try to eventually evict the pod from its node.\nWhen there are multiple elements, the lists of nodes corresponding to each\npodAffinityTerm are intersected, i.e. all terms must be satisfied.",
        ),
    ] = None


class Affinity(BaseModel):
    node_affinity: Annotated[
        Optional[NodeAffinity],
        Field(
            alias="nodeAffinity",
            description="Describes node affinity scheduling rules for the pod.",
        ),
    ] = None
    pod_affinity: Annotated[
        Optional[PodAffinity],
        Field(
            alias="podAffinity",
            description="Describes pod affinity scheduling rules (e.g. co-locate this pod in the same node, zone, etc. as some other pod(s)).",
        ),
    ] = None
    pod_anti_affinity: Annotated[
        Optional[PodAntiAffinity],
        Field(
            alias="podAntiAffinity",
            description="Describes pod anti-affinity scheduling rules (e.g. avoid putting this pod in the same node, zone, etc. as some other pod(s)).",
        ),
    ] = None


class ImagePullSecret(BaseModel):
    name: Annotated[
        Optional[str],
        Field(
            description="Name of the referent.\nThis field is effectively required, but due to backwards compatibility is\nallowed to be empty. Instances of this type with an empty value here are\nalmost certainly wrong.\nMore info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    ] = ""


class SeLinuxOptions(BaseModel):
    level: Annotated[
        Optional[str],
        Field(description="Level is SELinux level label that applies to the container."),
    ] = None
    role: Annotated[
        Optional[str],
        Field(description="Role is a SELinux role label that applies to the container."),
    ] = None
    type: Annotated[
        Optional[str],
        Field(description="Type is a SELinux type label that applies to the container."),
    ] = None
    user: Annotated[
        Optional[str],
        Field(description="User is a SELinux user label that applies to the container."),
    ] = None


class SeccompProfile(BaseModel):
    localhost_profile: Annotated[
        Optional[str],
        Field(
            alias="localhostProfile",
            description='localhostProfile indicates a profile defined in a file on the node should be used.\nThe profile must be preconfigured on the node to work.\nMust be a descending path, relative to the kubelet\'s configured seccomp profile location.\nMust be set if type is "Localhost". Must NOT be set for any other type.',
        ),
    ] = None
    type: Annotated[
        str,
        Field(
            description="type indicates which kind of seccomp profile will be applied.\nValid options are:\n\nLocalhost - a profile defined in a file on the node should be used.\nRuntimeDefault - the container runtime default profile should be used.\nUnconfined - no profile should be applied."
        ),
    ]


class Sysctl(BaseModel):
    name: Annotated[str, Field(description="Name of a property to set")]
    value: Annotated[str, Field(description="Value of a property to set")]


class SecurityContext(BaseModel):
    fs_group: Annotated[
        Optional[int],
        Field(
            alias="fsGroup",
            description="A special supplemental group that applies to all containers in a pod.\nSome volume types allow the Kubelet to change the ownership of that volume\nto be owned by the pod:\n\n1. The owning GID will be the FSGroup\n2. The setgid bit is set (new files created in the volume will be owned by FSGroup)\n3. The permission bits are OR'd with rw-rw----\n\nIf unset, the Kubelet will not modify the ownership and permissions of any volume.\nNote that this field cannot be set when spec.os.name is windows.",
        ),
    ] = None
    fs_group_change_policy: Annotated[
        Optional[str],
        Field(
            alias="fsGroupChangePolicy",
            description='fsGroupChangePolicy defines behavior of changing ownership and permission of the volume\nbefore being exposed inside Pod. This field will only apply to\nvolume types which support fsGroup based ownership(and permissions).\nIt will have no effect on ephemeral volume types such as: secret, configmaps\nand emptydir.\nValid values are "OnRootMismatch" and "Always". If not specified, "Always" is used.\nNote that this field cannot be set when spec.os.name is windows.',
        ),
    ] = None
    run_as_group: Annotated[
        Optional[int],
        Field(
            alias="runAsGroup",
            description="The GID to run the entrypoint of the container process.\nUses runtime default if unset.\nMay also be set in SecurityContext.  If set in both SecurityContext and\nPodSecurityContext, the value specified in SecurityContext takes precedence\nfor that container.\nNote that this field cannot be set when spec.os.name is windows.",
        ),
    ] = None
    run_as_non_root: Annotated[
        Optional[bool],
        Field(
            alias="runAsNonRoot",
            description="Indicates that the container must run as a non-root user.\nIf true, the Kubelet will validate the image at runtime to ensure that it\ndoes not run as UID 0 (root) and fail to start the container if it does.\nIf unset or false, no such validation will be performed.\nMay also be set in SecurityContext.  If set in both SecurityContext and\nPodSecurityContext, the value specified in SecurityContext takes precedence.",
        ),
    ] = None
    run_as_user: Annotated[
        Optional[int],
        Field(
            alias="runAsUser",
            description="The UID to run the entrypoint of the container process.\nDefaults to user specified in image metadata if unspecified.\nMay also be set in SecurityContext.  If set in both SecurityContext and\nPodSecurityContext, the value specified in SecurityContext takes precedence\nfor that container.\nNote that this field cannot be set when spec.os.name is windows.",
        ),
    ] = None
    se_linux_options: Annotated[
        Optional[SeLinuxOptions],
        Field(
            alias="seLinuxOptions",
            description="The SELinux context to be applied to all containers.\nIf unspecified, the container runtime will allocate a random SELinux context for each\ncontainer.  May also be set in SecurityContext.  If set in\nboth SecurityContext and PodSecurityContext, the value specified in SecurityContext\ntakes precedence for that container.\nNote that this field cannot be set when spec.os.name is windows.",
        ),
    ] = None
    seccomp_profile: Annotated[
        Optional[SeccompProfile],
        Field(
            alias="seccompProfile",
            description="The seccomp options to use by the containers in this pod.\nNote that this field cannot be set when spec.os.name is windows.",
        ),
    ] = None
    supplemental_groups: Annotated[
        Optional[List[int]],
        Field(
            alias="supplementalGroups",
            description="A list of groups applied to the first process run in each container, in addition\nto the container's primary GID, the fsGroup (if specified), and group memberships\ndefined in the container image for the uid of the container process. If unspecified,\nno additional groups are added to any container. Note that group memberships\ndefined in the container image for the uid of the container process are still effective,\neven if they are not included in this list.\nNote that this field cannot be set when spec.os.name is windows.",
        ),
    ] = None
    sysctls: Annotated[
        Optional[List[Sysctl]],
        Field(
            description="Sysctls hold a list of namespaced sysctls used for the pod. Pods with unsupported\nsysctls (by the container runtime) might fail to launch.\nNote that this field cannot be set when spec.os.name is windows."
        ),
    ] = None


class Toleration(BaseModel):
    effect: Annotated[
        Optional[str],
        Field(
            description="Effect indicates the taint effect to match. Empty means match all taint effects.\nWhen specified, allowed values are NoSchedule, PreferNoSchedule and NoExecute."
        ),
    ] = None
    key: Annotated[
        Optional[str],
        Field(
            description="Key is the taint key that the toleration applies to. Empty means match all taint keys.\nIf the key is empty, operator must be Exists; this combination means to match all values and all keys."
        ),
    ] = None
    operator: Annotated[
        Optional[str],
        Field(
            description="Operator represents a key's relationship to the value.\nValid operators are Exists and Equal. Defaults to Equal.\nExists is equivalent to wildcard for value, so that a pod can\ntolerate all taints of a particular category."
        ),
    ] = None
    toleration_seconds: Annotated[
        Optional[int],
        Field(
            alias="tolerationSeconds",
            description="TolerationSeconds represents the period of time the toleration (which must be\nof effect NoExecute, otherwise this field is ignored) tolerates the taint. By default,\nit is not set, which means tolerate the taint forever (do not evict). Zero and\nnegative values will be treated as 0 (evict immediately) by the system.",
        ),
    ] = None
    value: Annotated[
        Optional[str],
        Field(
            description="Value is the taint value the toleration matches to.\nIf the operator is Exists, the value should be empty, otherwise just a regular string."
        ),
    ] = None


class PodSpec(BaseModel):
    affinity: Annotated[
        Optional[Affinity], Field(description="If specified, the pod's scheduling constraints")
    ] = None
    image_pull_secrets: Annotated[
        Optional[List[ImagePullSecret]],
        Field(alias="imagePullSecrets", description="If specified, the pod's imagePullSecrets"),
    ] = None
    node_selector: Annotated[
        Optional[Dict[str, str]],
        Field(
            alias="nodeSelector",
            description="NodeSelector is a selector which must be true for the pod to fit on a node.\nSelector which must match a node's labels for the pod to be scheduled on that node.\nMore info: https://kubernetes.io/docs/concepts/configuration/assign-pod-node/",
        ),
    ] = None
    priority_class_name: Annotated[
        Optional[str],
        Field(alias="priorityClassName", description="If specified, the pod's priorityClassName."),
    ] = None
    security_context: Annotated[
        Optional[SecurityContext],
        Field(alias="securityContext", description="If specified, the pod's security context"),
    ] = None
    service_account_name: Annotated[
        Optional[str],
        Field(alias="serviceAccountName", description="If specified, the pod's service account"),
    ] = None
    tolerations: Annotated[
        Optional[List[Toleration]], Field(description="If specified, the pod's tolerations.")
    ] = None


class PodTemplate(BaseModel):
    metadata: Annotated[
        Optional[Metadata],
        Field(
            description="ObjectMeta overrides for the pod used to solve HTTP01 challenges.\nOnly the 'labels' and 'annotations' fields may be set.\nIf labels or annotations overlap with in-built values, the values here\nwill override the in-built values."
        ),
    ] = None
    spec: Annotated[
        Optional[PodSpec],
        Field(
            description="PodSpec defines overrides for the HTTP01 challenge solver pod.\nCheck ACMEChallengeSolverHTTP01IngressPodSpec to find out currently supported fields.\nAll other fields will be ignored."
        ),
    ] = None


class GatewayHttpRoute(BaseModel):
    labels: Annotated[
        Optional[Dict[str, str]],
        Field(
            description="Custom labels that will be applied to HTTPRoutes created by cert-manager\nwhile solving HTTP-01 challenges."
        ),
    ] = None
    parent_refs: Annotated[
        Optional[List[ParentRef]],
        Field(
            alias="parentRefs",
            description="When solving an HTTP-01 challenge, cert-manager creates an HTTPRoute.\ncert-manager needs to know which parentRefs should be used when creating\nthe HTTPRoute. Usually, the parentRef references a Gateway. See:\nhttps://gateway-api.sigs.k8s.io/api-types/httproute/#attaching-to-gateways",
        ),
    ] = None
    pod_template: Annotated[
        Optional[PodTemplate],
        Field(
            alias="podTemplate",
            description="Optional pod template used to configure the ACME challenge solver pods\nused for HTTP01 challenges.",
        ),
    ] = None
    service_type: Annotated[
        Optional[str],
        Field(
            alias="serviceType",
            description="Optional service type for Kubernetes solver service. Supported values\nare NodePort or ClusterIP. If unset, defaults to NodePort.",
        ),
    ] = None


class MetadataModel(BaseModel):
    annotations: Annotated[
        Optional[Dict[str, str]],
        Field(
            description="Annotations that should be added to the created ACME HTTP01 solver ingress."
        ),
    ] = None
    labels: Annotated[
        Optional[Dict[str, str]],
        Field(description="Labels that should be added to the created ACME HTTP01 solver ingress."),
    ] = None


class IngressTemplate(BaseModel):
    metadata: Annotated[
        Optional[MetadataModel],
        Field(
            description="ObjectMeta overrides for the ingress used to solve HTTP01 challenges.\nOnly the 'labels' and 'annotations' fields may be set.\nIf labels or annotations overlap with in-built values, the values here\nwill override the in-built values."
        ),
    ] = None


class Ingress(BaseModel):
    class_: Annotated[
        Optional[str],
        Field(
            alias="class",
            description="This field configures the annotation `kubernetes.io/ingress.class` when\ncreating Ingress resources to solve ACME challenges that use this\nchallenge solver. Only one of `class`, `name` or `ingressClassName` may\nbe specified.",
        ),
    ] = None
    ingress_class_name: Annotated[
        Optional[str],
        Field(
            alias="ingressClassName",
            description="This field configures the field `ingressClassName` on the created Ingress\nresources used to solve ACME challenges that use this challenge solver.\nThis is the recommended way of configuring the ingress class. Only one of\n`class`, `name` or `ingressClassName` may be specified.",
        ),
    ] = None
    ingress_template: Annotated[
        Optional[IngressTemplate],
        Field(
            alias="ingressTemplate",
            description="Optional ingress template used to configure the ACME challenge solver\ningress used for HTTP01 challenges.",
        ),
    ] = None
    name: Annotated[
        Optional[str],
        Field(
            description="The name of the ingress resource that should have ACME challenge solving\nroutes inserted into it in order to solve HTTP01 challenges.\nThis is typically used in conjunction with ingress controllers like\ningress-gce, which maintains a 1:1 mapping between external IPs and\ningress resources. Only one of `class`, `name` or `ingressClassName` may\nbe specified."
        ),
    ] = None
    pod_template: Annotated[
        Optional[PodTemplate],
        Field(
            alias="podTemplate",
            description="Optional pod template used to configure the ACME challenge solver pods\nused for HTTP01 challenges.",
        ),
    ] = None
    service_type: Annotated[
        Optional[str],
        Field(
            alias="serviceType",
            description="Optional service type for Kubernetes solver service. Supported values\nare NodePort or ClusterIP. If unset, defaults to NodePort.",
        ),
    ] = None


class Http01(BaseModel):
    gateway_http_route: Annotated[
        Optional[GatewayHttpRoute],
        Field(
            alias="gatewayHTTPRoute",
            description="The Gateway API is a sig-network community API that models service networking\nin Kubernetes (https://gateway-api.sigs.k8s.io/). The Gateway solver will\ncreate HTTPRoutes with the specified labels in the same namespace as the challenge.\nThis solver is experimental, and fields / behaviour may change in the future.",
        ),
    ] = None
    ingress: Annotated[
        Optional[Ingress],
        Field(
            description="The ingress based HTTP01 challenge solver will solve challenges by\ncreating or modifying Ingress resources in order to route requests for\n'/.well-known/acme-challenge/XYZ' to 'challenge solver' pods that are\nprovisioned by cert-manager for each Challenge to be completed."
        ),
    ] = None


class Selector(BaseModel):
    dns_names: Annotated[
        Optional[List[str]],
        Field(
            alias="dnsNames",
            description="List of DNSNames that this solver will be used to solve.\nIf specified and a match is found, a dnsNames selector will take\nprecedence over a dnsZones selector.\nIf multiple solvers match with the same dnsNames value, the solver\nwith the most matching labels in matchLabels will be selected.\nIf neither has more matches, the solver defined earlier in the list\nwill be selected.",
        ),
    ] = None
    dns_zones: Annotated[
        Optional[List[str]],
        Field(
            alias="dnsZones",
            description="List of DNSZones that this solver will be used to solve.\nThe most specific DNS zone match specified here will take precedence\nover other DNS zone matches, so a solver specifying sys.example.com\nwill be selected over one specifying example.com for the domain\nwww.sys.example.com.\nIf multiple solvers match with the same dnsZones value, the solver\nwith the most matching labels in matchLabels will be selected.\nIf neither has more matches, the solver defined earlier in the list\nwill be selected.",
        ),
    ] = None
    match_labels: Annotated[
        Optional[Dict[str, str]],
        Field(
            alias="matchLabels",
            description="A label selector that is used to refine the set of certificate's that\nthis challenge solver will apply to.",
        ),
    ] = None


class Solver(BaseModel):
    dns01: Annotated[
        Optional[Dns01],
        Field(
            description="Configures cert-manager to attempt to complete authorizations by\nperforming the DNS01 challenge flow."
        ),
    ] = None
    http01: Annotated[
        Optional[Http01],
        Field(
            description="Configures cert-manager to attempt to complete authorizations by\nperforming the HTTP01 challenge flow.\nIt is not possible to obtain certificates for wildcard domain names\n(e.g. `*.example.com`) using the HTTP01 challenge mechanism."
        ),
    ] = None
    selector: Annotated[
        Optional[Selector],
        Field(
            description="Selector selects a set of DNSNames on the Certificate resource that\nshould be solved using this challenge solver.\nIf not specified, the solver will be treated as the 'default' solver\nwith the lowest priority, i.e. if any other solver has a more specific\nmatch, it will be used instead."
        ),
    ] = None


class ChallengeSpec(BaseModel):
    authorization_url: Annotated[
        str,
        Field(
            alias="authorizationURL",
            description="The URL to the ACME Authorization resource that this\nchallenge is a part of.",
        ),
    ]
    dns_name: Annotated[
        str,
        Field(
            alias="dnsName",
            description="dnsName is the identifier that this challenge is for, e.g. example.com.\nIf the requested DNSName is a 'wildcard', this field MUST be set to the\nnon-wildcard domain, e.g. for `*.example.com`, it must be `example.com`.",
        ),
    ]
    issuer_ref: Annotated[
        IssuerRef,
        Field(
            alias="issuerRef",
            description="References a properly configured ACME-type Issuer which should\nbe used to create this Challenge.\nIf the Issuer does not exist, processing will be retried.\nIf the Issuer is not an 'ACME' Issuer, an error will be returned and the\nChallenge will be marked as failed.",
        ),
    ]
    key: Annotated[
        str,
        Field(
            description="The ACME challenge key for this challenge\nFor HTTP01 challenges, this is the value that must be responded with to\ncomplete the HTTP01 challenge in the format:\n`<private key JWK thumbprint>.<key from acme server for challenge>`.\nFor DNS01 challenges, this is the base64 encoded SHA256 sum of the\n`<private key JWK thumbprint>.<key from acme server for challenge>`\ntext that must be set as the TXT record content."
        ),
    ]
    solver: Annotated[
        Solver,
        Field(
            description="Contains the domain solving configuration that should be used to\nsolve this challenge resource."
        ),
    ]
    token: Annotated[
        str,
        Field(
            description="The ACME challenge token for this challenge.\nThis is the raw value returned from the ACME server."
        ),
    ]
    type: Annotated[
        Literal["HTTP-01", "DNS-01"],
        Field(
            description='The type of ACME challenge this resource represents.\nOne of "HTTP-01" or "DNS-01".'
        ),
    ]
    url: Annotated[
        str,
        Field(
            description="The URL of the ACME Challenge resource for this challenge.\nThis can be used to lookup details about the status of this challenge."
        ),
    ]
    wildcard: Annotated[
        Optional[bool],
        Field(
            description="wildcard will be true if this challenge is for a wildcard identifier,\nfor example '*.example.com'."
        ),
    ] = None


class ChallengeStatus(BaseModel):
    presented: Annotated[
        Optional[bool],
        Field(
            description="presented will be set to true if the challenge values for this challenge\nare currently 'presented'.\nThis *does not* imply the self check is passing. Only that the values\nhave been 'submitted' for the appropriate challenge mechanism (i.e. the\nDNS01 TXT record has been presented, or the HTTP01 configuration has been\nconfigured)."
        ),
    ] = None
    processing: Annotated[
        Optional[bool],
        Field(
            description="Used to denote whether this challenge should be processed or not.\nThis field will only be set to true by the 'scheduling' component.\nIt will only be set to false by the 'challenges' controller, after the\nchallenge has reached a final state or timed out.\nIf this field is set to false, the challenge controller will not take\nany more action."
        ),
    ] = None
    reason: Annotated[
        Optional[str],
        Field(
            description="Contains human readable information on why the Challenge is in the\ncurrent state."
        ),
    ] = None
    state: Annotated[
        Optional[
            Literal["valid", "ready", "pending", "processing", "invalid", "expired", "errored"]
        ],
        Field(
            description="Contains the current 'state' of the challenge.\nIf not set, the state of the challenge is unknown."
        ),
    ] = None


class OrderSpec(BaseModel):
    common_name: Annotated[
        Optional[str],
        Field(
            alias="commonName",
            description="CommonName is the common name as specified on the DER encoded CSR.\nIf specified, this value must also be present in `dnsNames` or `ipAddresses`.\nThis field must match the corresponding field on the DER encoded CSR.",
        ),
    ] = None
    dns_names: Annotated[
        Optional[List[str]],
        Field(
            alias="dnsNames",
            description="DNSNames is a list of DNS names that should be included as part of the Order\nvalidation process.\nThis field must match the corresponding field on the DER encoded CSR.",
        ),
    ] = None
    duration: Annotated[
        Optional[str],
        Field(
            description="Duration is the duration for the not after date for the requested certificate.\nthis is set on order creation as pe the ACME spec."
        ),
    ] = None
    ip_addresses: Annotated[
        Optional[List[str]],
        Field(
            alias="ipAddresses",
            description="IPAddresses is a list of IP addresses that should be included as part of the Order\nvalidation process.\nThis field must match the corresponding field on the DER encoded CSR.",
        ),
    ] = None
    issuer_ref: Annotated[
        IssuerRef,
        Field(
            alias="issuerRef",
            description="IssuerRef references a properly configured ACME-type Issuer which should\nbe used to create this Order.\nIf the Issuer does not exist, processing will be retried.\nIf the Issuer is not an 'ACME' Issuer, an error will be returned and the\nOrder will be marked as failed.",
        ),
    ]
    request: Annotated[
        str,
        Field(
            description="Certificate signing request bytes in DER encoding.\nThis will be used when finalizing the order.\nThis field must be set on the order."
        ),
    ]


class Challenge(Resource):
    token: Annotated[
        str,
        Field(
            description="Token is the token that must be presented for this challenge.\nThis is used to compute the 'key' that must also be presented."
        ),
    ]
    type: Annotated[
        str,
        Field(
            description="Type is the type of challenge being offered, e.g. 'http-01', 'dns-01',\n'tls-sni-01', etc.\nThis is the raw value retrieved from the ACME server.\nOnly 'http-01' and 'dns-01' are supported by cert-manager, other values\nwill be ignored."
        ),
    ]
    url: Annotated[
        str,
        Field(
            description="URL is the URL of this challenge. It can be used to retrieve additional\nmetadata about the Challenge from the ACME server."
        ),
    ]


class Authorization(BaseModel):
    challenges: Annotated[
        Optional[List[Challenge]],
        Field(
            description="Challenges specifies the challenge types offered by the ACME server.\nOne of these challenge types will be selected when validating the DNS\nname and an appropriate Challenge resource will be created to perform\nthe ACME challenge process."
        ),
    ] = None
    identifier: Annotated[
        Optional[str],
        Field(
            description="Identifier is the DNS name to be validated as part of this authorization"
        ),
    ] = None
    initial_state: Annotated[
        Optional[
            Literal["valid", "ready", "pending", "processing", "invalid", "expired", "errored"]
        ],
        Field(
            alias="initialState",
            description="InitialState is the initial state of the ACME authorization when first\nfetched from the ACME server.\nIf an Authorization is already 'valid', the Order controller will not\ncreate a Challenge resource for the authorization. This will occur when\nworking with an ACME server that enables 'authz reuse' (such as Let's\nEncrypt's production endpoint).\nIf not set and 'identifier' is set, the state is assumed to be pending\nand a Challenge will be created.",
        ),
    ] = None
    url: Annotated[
        str, Field(description="URL is the URL of the Authorization that must be completed")
    ]
    wildcard: Annotated[
        Optional[bool],
        Field(
            description="Wildcard will be true if this authorization is for a wildcard DNS name.\nIf this is true, the identifier will be the *non-wildcard* version of\nthe DNS name.\nFor example, if '*.example.com' is the DNS name being validated, this\nfield will be 'true' and the 'identifier' field will be 'example.com'."
        ),
    ] = None


class OrderStatus(BaseModel):
    authorizations: Annotated[
        Optional[List[Authorization]],
        Field(
            description="Authorizations contains data returned from the ACME server on what\nauthorizations must be completed in order to validate the DNS names\nspecified on the Order."
        ),
    ] = None
    certificate: Annotated[
        Optional[str],
        Field(
            description="Certificate is a copy of the PEM encoded certificate for this Order.\nThis field will be populated after the order has been successfully\nfinalized with the ACME server, and the order has transitioned to the\n'valid' state."
        ),
    ] = None
    failure_time: Annotated[
        Optional[datetime],
        Field(
            alias="failureTime",
            description="FailureTime stores the time that this order failed.\nThis is used to influence garbage collection and back-off.",
        ),
    ] = None
    finalize_url: Annotated[
        Optional[str],
        Field(
            alias="finalizeURL",
            description="FinalizeURL of the Order.\nThis is used to obtain certificates for this order once it has been completed.",
        ),
    ] = None
    reason: Annotated[
        Optional[str],
        Field(
            description="Reason optionally provides more information about a why the order is in\nthe current state."
        ),
    ] = None
    state: Annotated[
        Optional[
            Literal["valid", "ready", "pending", "processing", "invalid", "expired", "errored"]
        ],
        Field(
            description="State contains the current state of this Order resource.\nStates 'success' and 'expired' are 'final'"
        ),
    ] = None
    url: Annotated[
        Optional[str],
        Field(
            description="URL of the Order.\nThis will initially be empty when the resource is first created.\nThe Order controller will populate this field when the Order is first processed.\nThis field will be immutable after it is initially set."
        ),
    ] = None


class ChallengeModel(Resource):
    api_version: Annotated[
        Optional[Literal["acme.cert-manager.io/v1"]],
        Field(
            alias="apiVersion",
            description="APIVersion defines the versioned schema of this representation of an object.\nServers should convert recognized schemas to the latest internal value, and\nmay reject unrecognized values.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",
        ),
    ] = "acme.cert-manager.io/v1"
    kind: Annotated[
        Optional[Literal["Challenge"]],
        Field(
            description="Kind is a string value representing the REST resource this object represents.\nServers may infer this from the endpoint the client submits requests to.\nCannot be updated.\nIn CamelCase.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    ] = "Challenge"
    metadata: Optional[apimachinery.ObjectMeta] = None
    spec: ChallengeSpec
    status: Optional[ChallengeStatus] = None


class Order(Resource):
    api_version: Annotated[
        Optional[Literal["acme.cert-manager.io/v1"]],
        Field(
            alias="apiVersion",
            description="APIVersion defines the versioned schema of this representation of an object.\nServers should convert recognized schemas to the latest internal value, and\nmay reject unrecognized values.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",
        ),
    ] = "acme.cert-manager.io/v1"
    kind: Annotated[
        Optional[Literal["Order"]],
        Field(
            description="Kind is a string value representing the REST resource this object represents.\nServers may infer this from the endpoint the client submits requests to.\nCannot be updated.\nIn CamelCase.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    ] = "Order"
    metadata: Optional[apimachinery.ObjectMeta] = None
    spec: OrderSpec
    status: Optional[OrderStatus] = None
