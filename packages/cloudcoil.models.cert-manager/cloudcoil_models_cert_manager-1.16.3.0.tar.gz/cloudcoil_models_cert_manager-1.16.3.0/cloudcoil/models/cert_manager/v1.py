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


class CertificateRequestSpec(BaseModel):
    duration: Annotated[
        Optional[str],
        Field(
            description="Requested 'duration' (i.e. lifetime) of the Certificate. Note that the\nissuer may choose to ignore the requested duration, just like any other\nrequested attribute."
        ),
    ] = None
    extra: Annotated[
        Optional[Dict[str, List[str]]],
        Field(
            description="Extra contains extra attributes of the user that created the CertificateRequest.\nPopulated by the cert-manager webhook on creation and immutable."
        ),
    ] = None
    groups: Annotated[
        Optional[List[str]],
        Field(
            description="Groups contains group membership of the user that created the CertificateRequest.\nPopulated by the cert-manager webhook on creation and immutable."
        ),
    ] = None
    is_ca: Annotated[
        Optional[bool],
        Field(
            alias="isCA",
            description="Requested basic constraints isCA value. Note that the issuer may choose\nto ignore the requested isCA value, just like any other requested attribute.\n\nNOTE: If the CSR in the `Request` field has a BasicConstraints extension,\nit must have the same isCA value as specified here.\n\nIf true, this will automatically add the `cert sign` usage to the list\nof requested `usages`.",
        ),
    ] = None
    issuer_ref: Annotated[
        IssuerRef,
        Field(
            alias="issuerRef",
            description="Reference to the issuer responsible for issuing the certificate.\nIf the issuer is namespace-scoped, it must be in the same namespace\nas the Certificate. If the issuer is cluster-scoped, it can be used\nfrom any namespace.\n\nThe `name` field of the reference must always be specified.",
        ),
    ]
    request: Annotated[
        str,
        Field(
            description="The PEM-encoded X.509 certificate signing request to be submitted to the\nissuer for signing.\n\nIf the CSR has a BasicConstraints extension, its isCA attribute must\nmatch the `isCA` value of this CertificateRequest.\nIf the CSR has a KeyUsage extension, its key usages must match the\nkey usages in the `usages` field of this CertificateRequest.\nIf the CSR has a ExtKeyUsage extension, its extended key usages\nmust match the extended key usages in the `usages` field of this\nCertificateRequest."
        ),
    ]
    uid: Annotated[
        Optional[str],
        Field(
            description="UID contains the uid of the user that created the CertificateRequest.\nPopulated by the cert-manager webhook on creation and immutable."
        ),
    ] = None
    usages: Annotated[
        Optional[
            List[
                Literal[
                    "signing",
                    "digital signature",
                    "content commitment",
                    "key encipherment",
                    "key agreement",
                    "data encipherment",
                    "cert sign",
                    "crl sign",
                    "encipher only",
                    "decipher only",
                    "any",
                    "server auth",
                    "client auth",
                    "code signing",
                    "email protection",
                    "s/mime",
                    "ipsec end system",
                    "ipsec tunnel",
                    "ipsec user",
                    "timestamping",
                    "ocsp signing",
                    "microsoft sgc",
                    "netscape sgc",
                ]
            ]
        ],
        Field(
            description="Requested key usages and extended key usages.\n\nNOTE: If the CSR in the `Request` field has uses the KeyUsage or\nExtKeyUsage extension, these extensions must have the same values\nas specified here without any additional values.\n\nIf unset, defaults to `digital signature` and `key encipherment`."
        ),
    ] = None
    username: Annotated[
        Optional[str],
        Field(
            description="Username contains the name of the user that created the CertificateRequest.\nPopulated by the cert-manager webhook on creation and immutable."
        ),
    ] = None


class CertificateRequestCondition(BaseModel):
    last_transition_time: Annotated[
        Optional[datetime],
        Field(
            alias="lastTransitionTime",
            description="LastTransitionTime is the timestamp corresponding to the last status\nchange of this condition.",
        ),
    ] = None
    message: Annotated[
        Optional[str],
        Field(
            description="Message is a human readable description of the details of the last\ntransition, complementing reason."
        ),
    ] = None
    reason: Annotated[
        Optional[str],
        Field(
            description="Reason is a brief machine readable explanation for the condition's last\ntransition."
        ),
    ] = None
    status: Annotated[
        Literal["True", "False", "Unknown"],
        Field(description="Status of the condition, one of (`True`, `False`, `Unknown`)."),
    ]
    type: Annotated[
        str,
        Field(
            description="Type of the condition, known values are (`Ready`, `InvalidRequest`,\n`Approved`, `Denied`)."
        ),
    ]


class CertificateRequestStatus(BaseModel):
    ca: Annotated[
        Optional[str],
        Field(
            description="The PEM encoded X.509 certificate of the signer, also known as the CA\n(Certificate Authority).\nThis is set on a best-effort basis by different issuers.\nIf not set, the CA is assumed to be unknown/not available."
        ),
    ] = None
    certificate: Annotated[
        Optional[str],
        Field(
            description="The PEM encoded X.509 certificate resulting from the certificate\nsigning request.\nIf not set, the CertificateRequest has either not been completed or has\nfailed. More information on failure can be found by checking the\n`conditions` field."
        ),
    ] = None
    conditions: Annotated[
        Optional[List[CertificateRequestCondition]],
        Field(
            description="List of status conditions to indicate the status of a CertificateRequest.\nKnown condition types are `Ready`, `InvalidRequest`, `Approved` and `Denied`."
        ),
    ] = None
    failure_time: Annotated[
        Optional[datetime],
        Field(
            alias="failureTime",
            description="FailureTime stores the time that this CertificateRequest failed. This is\nused to influence garbage collection and back-off.",
        ),
    ] = None


class AdditionalOutputFormat(BaseModel):
    type: Annotated[
        Literal["DER", "CombinedPEM"],
        Field(
            description="Type is the name of the format type that should be written to the\nCertificate's target Secret."
        ),
    ]


class Jks(BaseModel):
    alias: Annotated[
        Optional[str],
        Field(
            description="Alias specifies the alias of the key in the keystore, required by the JKS format.\nIf not provided, the default alias `certificate` will be used."
        ),
    ] = None
    create: Annotated[
        bool,
        Field(
            description="Create enables JKS keystore creation for the Certificate.\nIf true, a file named `keystore.jks` will be created in the target\nSecret resource, encrypted using the password stored in\n`passwordSecretRef`.\nThe keystore file will be updated immediately.\nIf the issuer provided a CA certificate, a file named `truststore.jks`\nwill also be created in the target Secret resource, encrypted using the\npassword stored in `passwordSecretRef`\ncontaining the issuing Certificate Authority"
        ),
    ]
    password_secret_ref: Annotated[
        SecretRef,
        Field(
            alias="passwordSecretRef",
            description="PasswordSecretRef is a reference to a key in a Secret resource\ncontaining the password used to encrypt the JKS keystore.",
        ),
    ]


class Pkcs12(BaseModel):
    create: Annotated[
        bool,
        Field(
            description="Create enables PKCS12 keystore creation for the Certificate.\nIf true, a file named `keystore.p12` will be created in the target\nSecret resource, encrypted using the password stored in\n`passwordSecretRef`.\nThe keystore file will be updated immediately.\nIf the issuer provided a CA certificate, a file named `truststore.p12` will\nalso be created in the target Secret resource, encrypted using the\npassword stored in `passwordSecretRef` containing the issuing Certificate\nAuthority"
        ),
    ]
    password_secret_ref: Annotated[
        SecretRef,
        Field(
            alias="passwordSecretRef",
            description="PasswordSecretRef is a reference to a key in a Secret resource\ncontaining the password used to encrypt the PKCS12 keystore.",
        ),
    ]
    profile: Annotated[
        Optional[Literal["LegacyRC2", "LegacyDES", "Modern2023"]],
        Field(
            description="Profile specifies the key and certificate encryption algorithms and the HMAC algorithm\nused to create the PKCS12 keystore. Default value is `LegacyRC2` for backward compatibility.\n\nIf provided, allowed values are:\n`LegacyRC2`: Deprecated. Not supported by default in OpenSSL 3 or Java 20.\n`LegacyDES`: Less secure algorithm. Use this option for maximal compatibility.\n`Modern2023`: Secure algorithm. Use this option in case you have to always use secure algorithms\n(eg. because of company policy). Please note that the security of the algorithm is not that important\nin reality, because the unencrypted certificate and private key are also stored in the Secret."
        ),
    ] = None


class Keystores(BaseModel):
    jks: Annotated[
        Optional[Jks],
        Field(
            description="JKS configures options for storing a JKS keystore in the\n`spec.secretName` Secret resource."
        ),
    ] = None
    pkcs12: Annotated[
        Optional[Pkcs12],
        Field(
            description="PKCS12 configures options for storing a PKCS12 keystore in the\n`spec.secretName` Secret resource."
        ),
    ] = None


class Excluded(BaseModel):
    dns_domains: Annotated[
        Optional[List[str]],
        Field(
            alias="dnsDomains",
            description="DNSDomains is a list of DNS domains that are permitted or excluded.",
        ),
    ] = None
    email_addresses: Annotated[
        Optional[List[str]],
        Field(
            alias="emailAddresses",
            description="EmailAddresses is a list of Email Addresses that are permitted or excluded.",
        ),
    ] = None
    ip_ranges: Annotated[
        Optional[List[str]],
        Field(
            alias="ipRanges",
            description="IPRanges is a list of IP Ranges that are permitted or excluded.\nThis should be a valid CIDR notation.",
        ),
    ] = None
    uri_domains: Annotated[
        Optional[List[str]],
        Field(
            alias="uriDomains",
            description="URIDomains is a list of URI domains that are permitted or excluded.",
        ),
    ] = None


class NameConstraints(BaseModel):
    critical: Annotated[
        Optional[bool], Field(description="if true then the name constraints are marked critical.")
    ] = None
    excluded: Annotated[
        Optional[Excluded],
        Field(
            description="Excluded contains the constraints which must be disallowed. Any name matching a\nrestriction in the excluded field is invalid regardless\nof information appearing in the permitted"
        ),
    ] = None
    permitted: Annotated[
        Optional[Excluded],
        Field(description="Permitted contains the constraints in which the names must be located."),
    ] = None


class OtherName(BaseModel):
    oid: Annotated[
        Optional[str],
        Field(
            description='OID is the object identifier for the otherName SAN.\nThe object identifier must be expressed as a dotted string, for\nexample, "1.2.840.113556.1.4.221".'
        ),
    ] = None
    utf8_value: Annotated[
        Optional[str],
        Field(
            alias="utf8Value",
            description="utf8Value is the string value of the otherName SAN.\nThe utf8Value accepts any valid UTF8 string to set as value for the otherName SAN.",
        ),
    ] = None


class PrivateKey(BaseModel):
    algorithm: Annotated[
        Optional[Literal["RSA", "ECDSA", "Ed25519"]],
        Field(
            description="Algorithm is the private key algorithm of the corresponding private key\nfor this certificate.\n\nIf provided, allowed values are either `RSA`, `ECDSA` or `Ed25519`.\nIf `algorithm` is specified and `size` is not provided,\nkey size of 2048 will be used for `RSA` key algorithm and\nkey size of 256 will be used for `ECDSA` key algorithm.\nkey size is ignored when using the `Ed25519` key algorithm."
        ),
    ] = None
    encoding: Annotated[
        Optional[Literal["PKCS1", "PKCS8"]],
        Field(
            description="The private key cryptography standards (PKCS) encoding for this\ncertificate's private key to be encoded in.\n\nIf provided, allowed values are `PKCS1` and `PKCS8` standing for PKCS#1\nand PKCS#8, respectively.\nDefaults to `PKCS1` if not specified."
        ),
    ] = None
    rotation_policy: Annotated[
        Optional[Literal["Never", "Always"]],
        Field(
            alias="rotationPolicy",
            description="RotationPolicy controls how private keys should be regenerated when a\nre-issuance is being processed.\n\nIf set to `Never`, a private key will only be generated if one does not\nalready exist in the target `spec.secretName`. If one does exist but it\ndoes not have the correct algorithm or size, a warning will be raised\nto await user intervention.\nIf set to `Always`, a private key matching the specified requirements\nwill be generated whenever a re-issuance occurs.\nDefault is `Never` for backward compatibility.",
        ),
    ] = None
    size: Annotated[
        Optional[int],
        Field(
            description="Size is the key bit size of the corresponding private key for this certificate.\n\nIf `algorithm` is set to `RSA`, valid values are `2048`, `4096` or `8192`,\nand will default to `2048` if not specified.\nIf `algorithm` is set to `ECDSA`, valid values are `256`, `384` or `521`,\nand will default to `256` if not specified.\nIf `algorithm` is set to `Ed25519`, Size is ignored.\nNo other values are allowed."
        ),
    ] = None


class SecretTemplate(BaseModel):
    annotations: Annotated[
        Optional[Dict[str, str]],
        Field(
            description="Annotations is a key value map to be copied to the target Kubernetes Secret."
        ),
    ] = None
    labels: Annotated[
        Optional[Dict[str, str]],
        Field(
            description="Labels is a key value map to be copied to the target Kubernetes Secret."
        ),
    ] = None


class Subject(BaseModel):
    countries: Annotated[
        Optional[List[str]], Field(description="Countries to be used on the Certificate.")
    ] = None
    localities: Annotated[
        Optional[List[str]], Field(description="Cities to be used on the Certificate.")
    ] = None
    organizational_units: Annotated[
        Optional[List[str]],
        Field(
            alias="organizationalUnits",
            description="Organizational Units to be used on the Certificate.",
        ),
    ] = None
    organizations: Annotated[
        Optional[List[str]], Field(description="Organizations to be used on the Certificate.")
    ] = None
    postal_codes: Annotated[
        Optional[List[str]],
        Field(alias="postalCodes", description="Postal codes to be used on the Certificate."),
    ] = None
    provinces: Annotated[
        Optional[List[str]], Field(description="State/Provinces to be used on the Certificate.")
    ] = None
    serial_number: Annotated[
        Optional[str],
        Field(alias="serialNumber", description="Serial number to be used on the Certificate."),
    ] = None
    street_addresses: Annotated[
        Optional[List[str]],
        Field(
            alias="streetAddresses", description="Street addresses to be used on the Certificate."
        ),
    ] = None


class CertificateSpec(BaseModel):
    additional_output_formats: Annotated[
        Optional[List[AdditionalOutputFormat]],
        Field(
            alias="additionalOutputFormats",
            description="Defines extra output formats of the private key and signed certificate chain\nto be written to this Certificate's target Secret.\n\nThis is a Beta Feature enabled by default. It can be disabled with the\n`--feature-gates=AdditionalCertificateOutputFormats=false` option set on both\nthe controller and webhook components.",
        ),
    ] = None
    common_name: Annotated[
        Optional[str],
        Field(
            alias="commonName",
            description="Requested common name X509 certificate subject attribute.\nMore info: https://datatracker.ietf.org/doc/html/rfc5280#section-4.1.2.6\nNOTE: TLS clients will ignore this value when any subject alternative name is\nset (see https://tools.ietf.org/html/rfc6125#section-6.4.4).\n\nShould have a length of 64 characters or fewer to avoid generating invalid CSRs.\nCannot be set if the `literalSubject` field is set.",
        ),
    ] = None
    dns_names: Annotated[
        Optional[List[str]],
        Field(alias="dnsNames", description="Requested DNS subject alternative names."),
    ] = None
    duration: Annotated[
        Optional[str],
        Field(
            description="Requested 'duration' (i.e. lifetime) of the Certificate. Note that the\nissuer may choose to ignore the requested duration, just like any other\nrequested attribute.\n\nIf unset, this defaults to 90 days.\nMinimum accepted duration is 1 hour.\nValue must be in units accepted by Go time.ParseDuration https://golang.org/pkg/time/#ParseDuration."
        ),
    ] = None
    email_addresses: Annotated[
        Optional[List[str]],
        Field(alias="emailAddresses", description="Requested email subject alternative names."),
    ] = None
    encode_usages_in_request: Annotated[
        Optional[bool],
        Field(
            alias="encodeUsagesInRequest",
            description="Whether the KeyUsage and ExtKeyUsage extensions should be set in the encoded CSR.\n\nThis option defaults to true, and should only be disabled if the target\nissuer does not support CSRs with these X509 KeyUsage/ ExtKeyUsage extensions.",
        ),
    ] = None
    ip_addresses: Annotated[
        Optional[List[str]],
        Field(alias="ipAddresses", description="Requested IP address subject alternative names."),
    ] = None
    is_ca: Annotated[
        Optional[bool],
        Field(
            alias="isCA",
            description="Requested basic constraints isCA value.\nThe isCA value is used to set the `isCA` field on the created CertificateRequest\nresources. Note that the issuer may choose to ignore the requested isCA value, just\nlike any other requested attribute.\n\nIf true, this will automatically add the `cert sign` usage to the list\nof requested `usages`.",
        ),
    ] = None
    issuer_ref: Annotated[
        IssuerRef,
        Field(
            alias="issuerRef",
            description="Reference to the issuer responsible for issuing the certificate.\nIf the issuer is namespace-scoped, it must be in the same namespace\nas the Certificate. If the issuer is cluster-scoped, it can be used\nfrom any namespace.\n\nThe `name` field of the reference must always be specified.",
        ),
    ]
    keystores: Annotated[
        Optional[Keystores],
        Field(
            description="Additional keystore output formats to be stored in the Certificate's Secret."
        ),
    ] = None
    literal_subject: Annotated[
        Optional[str],
        Field(
            alias="literalSubject",
            description='Requested X.509 certificate subject, represented using the LDAP "String\nRepresentation of a Distinguished Name" [1].\nImportant: the LDAP string format also specifies the order of the attributes\nin the subject, this is important when issuing certs for LDAP authentication.\nExample: `CN=foo,DC=corp,DC=example,DC=com`\nMore info [1]: https://datatracker.ietf.org/doc/html/rfc4514\nMore info: https://github.com/cert-manager/cert-manager/issues/3203\nMore info: https://github.com/cert-manager/cert-manager/issues/4424\n\nCannot be set if the `subject` or `commonName` field is set.',
        ),
    ] = None
    name_constraints: Annotated[
        Optional[NameConstraints],
        Field(
            alias="nameConstraints",
            description="x.509 certificate NameConstraint extension which MUST NOT be used in a non-CA certificate.\nMore Info: https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.10\n\nThis is an Alpha Feature and is only enabled with the\n`--feature-gates=NameConstraints=true` option set on both\nthe controller and webhook components.",
        ),
    ] = None
    other_names: Annotated[
        Optional[List[OtherName]],
        Field(
            alias="otherNames",
            description="`otherNames` is an escape hatch for SAN that allows any type. We currently restrict the support to string like otherNames, cf RFC 5280 p 37\nAny UTF8 String valued otherName can be passed with by setting the keys oid: x.x.x.x and UTF8Value: somevalue for `otherName`.\nMost commonly this would be UPN set with oid: 1.3.6.1.4.1.311.20.2.3\nYou should ensure that any OID passed is valid for the UTF8String type as we do not explicitly validate this.",
        ),
    ] = None
    private_key: Annotated[
        Optional[PrivateKey],
        Field(
            alias="privateKey",
            description="Private key options. These include the key algorithm and size, the used\nencoding and the rotation policy.",
        ),
    ] = None
    renew_before: Annotated[
        Optional[str],
        Field(
            alias="renewBefore",
            description="How long before the currently issued certificate's expiry cert-manager should\nrenew the certificate. For example, if a certificate is valid for 60 minutes,\nand `renewBefore=10m`, cert-manager will begin to attempt to renew the certificate\n50 minutes after it was issued (i.e. when there are 10 minutes remaining until\nthe certificate is no longer valid).\n\nNOTE: The actual lifetime of the issued certificate is used to determine the\nrenewal time. If an issuer returns a certificate with a different lifetime than\nthe one requested, cert-manager will use the lifetime of the issued certificate.\n\nIf unset, this defaults to 1/3 of the issued certificate's lifetime.\nMinimum accepted value is 5 minutes.\nValue must be in units accepted by Go time.ParseDuration https://golang.org/pkg/time/#ParseDuration.\nCannot be set if the `renewBeforePercentage` field is set.",
        ),
    ] = None
    renew_before_percentage: Annotated[
        Optional[int],
        Field(
            alias="renewBeforePercentage",
            description="`renewBeforePercentage` is like `renewBefore`, except it is a relative percentage\nrather than an absolute duration. For example, if a certificate is valid for 60\nminutes, and  `renewBeforePercentage=25`, cert-manager will begin to attempt to\nrenew the certificate 45 minutes after it was issued (i.e. when there are 15\nminutes (25%) remaining until the certificate is no longer valid).\n\nNOTE: The actual lifetime of the issued certificate is used to determine the\nrenewal time. If an issuer returns a certificate with a different lifetime than\nthe one requested, cert-manager will use the lifetime of the issued certificate.\n\nValue must be an integer in the range (0,100). The minimum effective\n`renewBefore` derived from the `renewBeforePercentage` and `duration` fields is 5\nminutes.\nCannot be set if the `renewBefore` field is set.",
        ),
    ] = None
    revision_history_limit: Annotated[
        Optional[int],
        Field(
            alias="revisionHistoryLimit",
            description="The maximum number of CertificateRequest revisions that are maintained in\nthe Certificate's history. Each revision represents a single `CertificateRequest`\ncreated by this Certificate, either when it was created, renewed, or Spec\nwas changed. Revisions will be removed by oldest first if the number of\nrevisions exceeds this number.\n\nIf set, revisionHistoryLimit must be a value of `1` or greater.\nIf unset (`nil`), revisions will not be garbage collected.\nDefault value is `nil`.",
        ),
    ] = None
    secret_name: Annotated[
        str,
        Field(
            alias="secretName",
            description="Name of the Secret resource that will be automatically created and\nmanaged by this Certificate resource. It will be populated with a\nprivate key and certificate, signed by the denoted issuer. The Secret\nresource lives in the same namespace as the Certificate resource.",
        ),
    ]
    secret_template: Annotated[
        Optional[SecretTemplate],
        Field(
            alias="secretTemplate",
            description="Defines annotations and labels to be copied to the Certificate's Secret.\nLabels and annotations on the Secret will be changed as they appear on the\nSecretTemplate when added or removed. SecretTemplate annotations are added\nin conjunction with, and cannot overwrite, the base set of annotations\ncert-manager sets on the Certificate's Secret.",
        ),
    ] = None
    subject: Annotated[
        Optional[Subject],
        Field(
            description="Requested set of X509 certificate subject attributes.\nMore info: https://datatracker.ietf.org/doc/html/rfc5280#section-4.1.2.6\n\nThe common name attribute is specified separately in the `commonName` field.\nCannot be set if the `literalSubject` field is set."
        ),
    ] = None
    uris: Annotated[
        Optional[List[str]], Field(description="Requested URI subject alternative names.")
    ] = None
    usages: Annotated[
        Optional[
            List[
                Literal[
                    "signing",
                    "digital signature",
                    "content commitment",
                    "key encipherment",
                    "key agreement",
                    "data encipherment",
                    "cert sign",
                    "crl sign",
                    "encipher only",
                    "decipher only",
                    "any",
                    "server auth",
                    "client auth",
                    "code signing",
                    "email protection",
                    "s/mime",
                    "ipsec end system",
                    "ipsec tunnel",
                    "ipsec user",
                    "timestamping",
                    "ocsp signing",
                    "microsoft sgc",
                    "netscape sgc",
                ]
            ]
        ],
        Field(
            description="Requested key usages and extended key usages.\nThese usages are used to set the `usages` field on the created CertificateRequest\nresources. If `encodeUsagesInRequest` is unset or set to `true`, the usages\nwill additionally be encoded in the `request` field which contains the CSR blob.\n\nIf unset, defaults to `digital signature` and `key encipherment`."
        ),
    ] = None


class CertificateCondition(BaseModel):
    last_transition_time: Annotated[
        Optional[datetime],
        Field(
            alias="lastTransitionTime",
            description="LastTransitionTime is the timestamp corresponding to the last status\nchange of this condition.",
        ),
    ] = None
    message: Annotated[
        Optional[str],
        Field(
            description="Message is a human readable description of the details of the last\ntransition, complementing reason."
        ),
    ] = None
    observed_generation: Annotated[
        Optional[int],
        Field(
            alias="observedGeneration",
            description="If set, this represents the .metadata.generation that the condition was\nset based upon.\nFor instance, if .metadata.generation is currently 12, but the\n.status.condition[x].observedGeneration is 9, the condition is out of date\nwith respect to the current state of the Certificate.",
        ),
    ] = None
    reason: Annotated[
        Optional[str],
        Field(
            description="Reason is a brief machine readable explanation for the condition's last\ntransition."
        ),
    ] = None
    status: Annotated[
        Literal["True", "False", "Unknown"],
        Field(description="Status of the condition, one of (`True`, `False`, `Unknown`)."),
    ]
    type: Annotated[
        str, Field(description="Type of the condition, known values are (`Ready`, `Issuing`).")
    ]


class CertificateStatus(BaseModel):
    conditions: Annotated[
        Optional[List[CertificateCondition]],
        Field(
            description="List of status conditions to indicate the status of certificates.\nKnown condition types are `Ready` and `Issuing`."
        ),
    ] = None
    failed_issuance_attempts: Annotated[
        Optional[int],
        Field(
            alias="failedIssuanceAttempts",
            description="The number of continuous failed issuance attempts up till now. This\nfield gets removed (if set) on a successful issuance and gets set to\n1 if unset and an issuance has failed. If an issuance has failed, the\ndelay till the next issuance will be calculated using formula\ntime.Hour * 2 ^ (failedIssuanceAttempts - 1).",
        ),
    ] = None
    last_failure_time: Annotated[
        Optional[datetime],
        Field(
            alias="lastFailureTime",
            description="LastFailureTime is set only if the latest issuance for this\nCertificate failed and contains the time of the failure. If an\nissuance has failed, the delay till the next issuance will be\ncalculated using formula time.Hour * 2 ^ (failedIssuanceAttempts -\n1). If the latest issuance has succeeded this field will be unset.",
        ),
    ] = None
    next_private_key_secret_name: Annotated[
        Optional[str],
        Field(
            alias="nextPrivateKeySecretName",
            description="The name of the Secret resource containing the private key to be used\nfor the next certificate iteration.\nThe keymanager controller will automatically set this field if the\n`Issuing` condition is set to `True`.\nIt will automatically unset this field when the Issuing condition is\nnot set or False.",
        ),
    ] = None
    not_after: Annotated[
        Optional[datetime],
        Field(
            alias="notAfter",
            description="The expiration time of the certificate stored in the secret named\nby this resource in `spec.secretName`.",
        ),
    ] = None
    not_before: Annotated[
        Optional[datetime],
        Field(
            alias="notBefore",
            description="The time after which the certificate stored in the secret named\nby this resource in `spec.secretName` is valid.",
        ),
    ] = None
    renewal_time: Annotated[
        Optional[datetime],
        Field(
            alias="renewalTime",
            description="RenewalTime is the time at which the certificate will be next\nrenewed.\nIf not set, no upcoming renewal is scheduled.",
        ),
    ] = None
    revision: Annotated[
        Optional[int],
        Field(
            description="The current 'revision' of the certificate as issued.\n\nWhen a CertificateRequest resource is created, it will have the\n`cert-manager.io/certificate-revision` set to one greater than the\ncurrent value of this field.\n\nUpon issuance, this field will be set to the value of the annotation\non the CertificateRequest resource used to issue the certificate.\n\nPersisting the value on the CertificateRequest resource allows the\ncertificates controller to know whether a request is part of an old\nissuance or if it is part of the ongoing revision's issuance by\nchecking if the revision value in the annotation is greater than this\nfield."
        ),
    ] = None


class ExternalAccountBinding(BaseModel):
    key_algorithm: Annotated[
        Optional[Literal["HS256", "HS384", "HS512"]],
        Field(
            alias="keyAlgorithm",
            description="Deprecated: keyAlgorithm field exists for historical compatibility\nreasons and should not be used. The algorithm is now hardcoded to HS256\nin golang/x/crypto/acme.",
        ),
    ] = None
    key_id: Annotated[
        str,
        Field(
            alias="keyID",
            description="keyID is the ID of the CA key that the External Account is bound to.",
        ),
    ]
    key_secret_ref: Annotated[
        SecretRef,
        Field(
            alias="keySecretRef",
            description="keySecretRef is a Secret Key Selector referencing a data item in a Kubernetes\nSecret which holds the symmetric MAC key of the External Account Binding.\nThe `key` is the index string that is paired with the key data in the\nSecret and should not be confused with the key data itself, or indeed with\nthe External Account Binding keyID above.\nThe secret key stored in the Secret **must** be un-padded, base64 URL\nencoded data.",
        ),
    ]


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


class Acme(BaseModel):
    ca_bundle: Annotated[
        Optional[str],
        Field(
            alias="caBundle",
            description="Base64-encoded bundle of PEM CAs which can be used to validate the certificate\nchain presented by the ACME server.\nMutually exclusive with SkipTLSVerify; prefer using CABundle to prevent various\nkinds of security vulnerabilities.\nIf CABundle and SkipTLSVerify are unset, the system certificate bundle inside\nthe container is used to validate the TLS connection.",
        ),
    ] = None
    disable_account_key_generation: Annotated[
        Optional[bool],
        Field(
            alias="disableAccountKeyGeneration",
            description="Enables or disables generating a new ACME account key.\nIf true, the Issuer resource will *not* request a new account but will expect\nthe account key to be supplied via an existing secret.\nIf false, the cert-manager system will generate a new ACME account key\nfor the Issuer.\nDefaults to false.",
        ),
    ] = None
    email: Annotated[
        Optional[str],
        Field(
            description="Email is the email address to be associated with the ACME account.\nThis field is optional, but it is strongly recommended to be set.\nIt will be used to contact you in case of issues with your account or\ncertificates, including expiry notification emails.\nThis field may be updated after the account is initially registered."
        ),
    ] = None
    enable_duration_feature: Annotated[
        Optional[bool],
        Field(
            alias="enableDurationFeature",
            description="Enables requesting a Not After date on certificates that matches the\nduration of the certificate. This is not supported by all ACME servers\nlike Let's Encrypt. If set to true when the ACME server does not support\nit, it will create an error on the Order.\nDefaults to false.",
        ),
    ] = None
    external_account_binding: Annotated[
        Optional[ExternalAccountBinding],
        Field(
            alias="externalAccountBinding",
            description="ExternalAccountBinding is a reference to a CA external account of the ACME\nserver.\nIf set, upon registration cert-manager will attempt to associate the given\nexternal account credentials with the registered ACME account.",
        ),
    ] = None
    preferred_chain: Annotated[
        Optional[str],
        Field(
            alias="preferredChain",
            description="PreferredChain is the chain to use if the ACME server outputs multiple.\nPreferredChain is no guarantee that this one gets delivered by the ACME\nendpoint.\nFor example, for Let's Encrypt's DST crosssign you would use:\n\"DST Root CA X3\" or \"ISRG Root X1\" for the newer Let's Encrypt root CA.\nThis value picks the first certificate bundle in the combined set of\nACME default and alternative chains that has a root-most certificate with\nthis value as its issuer's commonname.",
            max_length=64,
        ),
    ] = None
    private_key_secret_ref: Annotated[
        SecretRef,
        Field(
            alias="privateKeySecretRef",
            description="PrivateKey is the name of a Kubernetes Secret resource that will be used to\nstore the automatically generated ACME account private key.\nOptionally, a `key` may be specified to select a specific entry within\nthe named Secret resource.\nIf `key` is not specified, a default of `tls.key` will be used.",
        ),
    ]
    server: Annotated[
        str,
        Field(
            description="Server is the URL used to access the ACME server's 'directory' endpoint.\nFor example, for Let's Encrypt's staging endpoint, you would use:\n\"https://acme-staging-v02.api.letsencrypt.org/directory\".\nOnly ACME v2 endpoints (i.e. RFC 8555) are supported."
        ),
    ]
    skip_tls_verify: Annotated[
        Optional[bool],
        Field(
            alias="skipTLSVerify",
            description="INSECURE: Enables or disables validation of the ACME server TLS certificate.\nIf true, requests to the ACME server will not have the TLS certificate chain\nvalidated.\nMutually exclusive with CABundle; prefer using CABundle to prevent various\nkinds of security vulnerabilities.\nOnly enable this option in development environments.\nIf CABundle and SkipTLSVerify are unset, the system certificate bundle inside\nthe container is used to validate the TLS connection.\nDefaults to false.",
        ),
    ] = None
    solvers: Annotated[
        Optional[List[Solver]],
        Field(
            description="Solvers is a list of challenge solvers that will be used to solve\nACME challenges for the matching domains.\nSolver configurations must be provided in order to obtain certificates\nfrom an ACME server.\nFor more information, see: https://cert-manager.io/docs/configuration/acme/"
        ),
    ] = None


class Ca(BaseModel):
    crl_distribution_points: Annotated[
        Optional[List[str]],
        Field(
            alias="crlDistributionPoints",
            description="The CRL distribution points is an X.509 v3 certificate extension which identifies\nthe location of the CRL from which the revocation of this certificate can be checked.\nIf not set, certificates will be issued without distribution points set.",
        ),
    ] = None
    issuing_certificate_ur_ls: Annotated[
        Optional[List[str]],
        Field(
            alias="issuingCertificateURLs",
            description='IssuingCertificateURLs is a list of URLs which this issuer should embed into certificates\nit creates. See https://www.rfc-editor.org/rfc/rfc5280#section-4.2.2.1 for more details.\nAs an example, such a URL might be "http://ca.domain.com/ca.crt".',
        ),
    ] = None
    ocsp_servers: Annotated[
        Optional[List[str]],
        Field(
            alias="ocspServers",
            description='The OCSP server list is an X.509 v3 extension that defines a list of\nURLs of OCSP responders. The OCSP responders can be queried for the\nrevocation status of an issued certificate. If not set, the\ncertificate will be issued with no OCSP servers set. For example, an\nOCSP server URL could be "http://ocsp.int-x3.letsencrypt.org".',
        ),
    ] = None
    secret_name: Annotated[
        str,
        Field(
            alias="secretName",
            description="SecretName is the name of the secret used to sign Certificates issued\nby this Issuer.",
        ),
    ]


class SelfSigned(BaseModel):
    crl_distribution_points: Annotated[
        Optional[List[str]],
        Field(
            alias="crlDistributionPoints",
            description="The CRL distribution points is an X.509 v3 certificate extension which identifies\nthe location of the CRL from which the revocation of this certificate can be checked.\nIf not set certificate will be issued without CDP. Values are strings.",
        ),
    ] = None


class AppRole(BaseModel):
    path: Annotated[
        str,
        Field(
            description='Path where the App Role authentication backend is mounted in Vault, e.g:\n"approle"'
        ),
    ]
    role_id: Annotated[
        str,
        Field(
            alias="roleId",
            description="RoleID configured in the App Role authentication backend when setting\nup the authentication backend in Vault.",
        ),
    ]
    secret_ref: Annotated[
        SecretRef,
        Field(
            alias="secretRef",
            description="Reference to a key in a Secret that contains the App Role secret used\nto authenticate with Vault.\nThe `key` field must be specified and denotes which entry within the Secret\nresource is used as the app role secret.",
        ),
    ]


class ClientCertificate(BaseModel):
    mount_path: Annotated[
        Optional[str],
        Field(
            alias="mountPath",
            description='The Vault mountPath here is the mount path to use when authenticating with\nVault. For example, setting a value to `/v1/auth/foo`, will use the path\n`/v1/auth/foo/login` to authenticate with Vault. If unspecified, the\ndefault value "/v1/auth/cert" will be used.',
        ),
    ] = None
    name: Annotated[
        Optional[str],
        Field(
            description="Name of the certificate role to authenticate against.\nIf not set, matching any certificate role, if available."
        ),
    ] = None
    secret_name: Annotated[
        Optional[str],
        Field(
            alias="secretName",
            description='Reference to Kubernetes Secret of type "kubernetes.io/tls" (hence containing\ntls.crt and tls.key) used to authenticate to Vault using TLS client\nauthentication.',
        ),
    ] = None


class ServiceAccountRefModel(BaseModel):
    audiences: Annotated[
        Optional[List[str]],
        Field(
            description="TokenAudiences is an optional list of extra audiences to include in the token passed to Vault. The default token\nconsisting of the issuer's namespace and name is always included."
        ),
    ] = None
    name: Annotated[str, Field(description="Name of the ServiceAccount used to request a token.")]


class KubernetesVaultAuth(BaseModel):
    mount_path: Annotated[
        Optional[str],
        Field(
            alias="mountPath",
            description='The Vault mountPath here is the mount path to use when authenticating with\nVault. For example, setting a value to `/v1/auth/foo`, will use the path\n`/v1/auth/foo/login` to authenticate with Vault. If unspecified, the\ndefault value "/v1/auth/kubernetes" will be used.',
        ),
    ] = None
    role: Annotated[
        str,
        Field(
            description="A required field containing the Vault Role to assume. A Role binds a\nKubernetes ServiceAccount with a set of Vault policies."
        ),
    ]
    secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="secretRef",
            description="The required Secret field containing a Kubernetes ServiceAccount JWT used\nfor authenticating with Vault. Use of 'ambient credentials' is not\nsupported.",
        ),
    ] = None
    service_account_ref: Annotated[
        Optional[ServiceAccountRefModel],
        Field(
            alias="serviceAccountRef",
            description='A reference to a service account that will be used to request a bound\ntoken (also known as "projected token"). Compared to using "secretRef",\nusing this field means that you don\'t rely on statically bound tokens. To\nuse this field, you must configure an RBAC rule to let cert-manager\nrequest a token.',
        ),
    ] = None


class VaultAuth(BaseModel):
    app_role: Annotated[
        Optional[AppRole],
        Field(
            alias="appRole",
            description="AppRole authenticates with Vault using the App Role auth mechanism,\nwith the role and secret stored in a Kubernetes Secret resource.",
        ),
    ] = None
    client_certificate: Annotated[
        Optional[ClientCertificate],
        Field(
            alias="clientCertificate",
            description="ClientCertificate authenticates with Vault by presenting a client\ncertificate during the request's TLS handshake.\nWorks only when using HTTPS protocol.",
        ),
    ] = None
    kubernetes: Annotated[
        Optional[KubernetesVaultAuth],
        Field(
            description="Kubernetes authenticates with Vault by passing the ServiceAccount\ntoken stored in the named Secret resource to the Vault server."
        ),
    ] = None
    token_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="tokenSecretRef",
            description="TokenSecretRef authenticates with Vault by presenting a token.",
        ),
    ] = None


class Vault(BaseModel):
    auth: Annotated[
        VaultAuth,
        Field(description="Auth configures how cert-manager authenticates with the Vault server."),
    ]
    ca_bundle: Annotated[
        Optional[str],
        Field(
            alias="caBundle",
            description="Base64-encoded bundle of PEM CAs which will be used to validate the certificate\nchain presented by Vault. Only used if using HTTPS to connect to Vault and\nignored for HTTP connections.\nMutually exclusive with CABundleSecretRef.\nIf neither CABundle nor CABundleSecretRef are defined, the certificate bundle in\nthe cert-manager controller container is used to validate the TLS connection.",
        ),
    ] = None
    ca_bundle_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="caBundleSecretRef",
            description="Reference to a Secret containing a bundle of PEM-encoded CAs to use when\nverifying the certificate chain presented by Vault when using HTTPS.\nMutually exclusive with CABundle.\nIf neither CABundle nor CABundleSecretRef are defined, the certificate bundle in\nthe cert-manager controller container is used to validate the TLS connection.\nIf no key for the Secret is specified, cert-manager will default to 'ca.crt'.",
        ),
    ] = None
    client_cert_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="clientCertSecretRef",
            description="Reference to a Secret containing a PEM-encoded Client Certificate to use when the\nVault server requires mTLS.",
        ),
    ] = None
    client_key_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="clientKeySecretRef",
            description="Reference to a Secret containing a PEM-encoded Client Private Key to use when the\nVault server requires mTLS.",
        ),
    ] = None
    namespace: Annotated[
        Optional[str],
        Field(
            description='Name of the vault namespace. Namespaces is a set of features within Vault Enterprise that allows Vault environments to support Secure Multi-tenancy. e.g: "ns1"\nMore about namespaces can be found here https://www.vaultproject.io/docs/enterprise/namespaces'
        ),
    ] = None
    path: Annotated[
        str,
        Field(
            description='Path is the mount path of the Vault PKI backend\'s `sign` endpoint, e.g:\n"my_pki_mount/sign/my-role-name".'
        ),
    ]
    server: Annotated[
        str,
        Field(
            description='Server is the connection address for the Vault server, e.g: "https://vault.example.com:8200".'
        ),
    ]


class Cloud(BaseModel):
    api_token_secret_ref: Annotated[
        SecretRef,
        Field(
            alias="apiTokenSecretRef",
            description="APITokenSecretRef is a secret key selector for the Venafi Cloud API token.",
        ),
    ]
    url: Annotated[
        Optional[str],
        Field(
            description='URL is the base URL for Venafi Cloud.\nDefaults to "https://api.venafi.cloud/v1".'
        ),
    ] = None


class CredentialsRef(BaseModel):
    name: Annotated[
        str,
        Field(
            description="Name of the resource being referred to.\nMore info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names"
        ),
    ]


class Tpp(BaseModel):
    ca_bundle: Annotated[
        Optional[str],
        Field(
            alias="caBundle",
            description="Base64-encoded bundle of PEM CAs which will be used to validate the certificate\nchain presented by the TPP server. Only used if using HTTPS; ignored for HTTP.\nIf undefined, the certificate bundle in the cert-manager controller container\nis used to validate the chain.",
        ),
    ] = None
    ca_bundle_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="caBundleSecretRef",
            description="Reference to a Secret containing a base64-encoded bundle of PEM CAs\nwhich will be used to validate the certificate chain presented by the TPP server.\nOnly used if using HTTPS; ignored for HTTP. Mutually exclusive with CABundle.\nIf neither CABundle nor CABundleSecretRef is defined, the certificate bundle in\nthe cert-manager controller container is used to validate the TLS connection.",
        ),
    ] = None
    credentials_ref: Annotated[
        CredentialsRef,
        Field(
            alias="credentialsRef",
            description="CredentialsRef is a reference to a Secret containing the Venafi TPP API credentials.\nThe secret must contain the key 'access-token' for the Access Token Authentication,\nor two keys, 'username' and 'password' for the API Keys Authentication.",
        ),
    ]
    url: Annotated[
        str,
        Field(
            description='URL is the base URL for the vedsdk endpoint of the Venafi TPP instance,\nfor example: "https://tpp.example.com/vedsdk".'
        ),
    ]


class Venafi(BaseModel):
    cloud: Annotated[
        Optional[Cloud],
        Field(
            description="Cloud specifies the Venafi cloud configuration settings.\nOnly one of TPP or Cloud may be specified."
        ),
    ] = None
    tpp: Annotated[
        Optional[Tpp],
        Field(
            description="TPP specifies Trust Protection Platform configuration settings.\nOnly one of TPP or Cloud may be specified."
        ),
    ] = None
    zone: Annotated[
        str,
        Field(
            description="Zone is the Venafi Policy Zone to use for this issuer.\nAll requests made to the Venafi platform will be restricted by the named\nzone policy.\nThis field is required."
        ),
    ]


class ClusterIssuerSpec(BaseModel):
    acme: Annotated[
        Optional[Acme],
        Field(
            description="ACME configures this issuer to communicate with a RFC8555 (ACME) server\nto obtain signed x509 certificates."
        ),
    ] = None
    ca: Annotated[
        Optional[Ca],
        Field(
            description="CA configures this issuer to sign certificates using a signing CA keypair\nstored in a Secret resource.\nThis is used to build internal PKIs that are managed by cert-manager."
        ),
    ] = None
    self_signed: Annotated[
        Optional[SelfSigned],
        Field(
            alias="selfSigned",
            description="SelfSigned configures this issuer to 'self sign' certificates using the\nprivate key used to create the CertificateRequest object.",
        ),
    ] = None
    vault: Annotated[
        Optional[Vault],
        Field(
            description="Vault configures this issuer to sign certificates using a HashiCorp Vault\nPKI backend."
        ),
    ] = None
    venafi: Annotated[
        Optional[Venafi],
        Field(
            description="Venafi configures this issuer to sign certificates using a Venafi TPP\nor Venafi Cloud policy zone."
        ),
    ] = None


class AcmeModel(BaseModel):
    last_private_key_hash: Annotated[
        Optional[str],
        Field(
            alias="lastPrivateKeyHash",
            description="LastPrivateKeyHash is a hash of the private key associated with the latest\nregistered ACME account, in order to track changes made to registered account\nassociated with the Issuer",
        ),
    ] = None
    last_registered_email: Annotated[
        Optional[str],
        Field(
            alias="lastRegisteredEmail",
            description="LastRegisteredEmail is the email associated with the latest registered\nACME account, in order to track changes made to registered account\nassociated with the  Issuer",
        ),
    ] = None
    uri: Annotated[
        Optional[str],
        Field(
            description="URI is the unique account identifier, which can also be used to retrieve\naccount details from the CA"
        ),
    ] = None


class IssuerCondition(BaseModel):
    last_transition_time: Annotated[
        Optional[datetime],
        Field(
            alias="lastTransitionTime",
            description="LastTransitionTime is the timestamp corresponding to the last status\nchange of this condition.",
        ),
    ] = None
    message: Annotated[
        Optional[str],
        Field(
            description="Message is a human readable description of the details of the last\ntransition, complementing reason."
        ),
    ] = None
    observed_generation: Annotated[
        Optional[int],
        Field(
            alias="observedGeneration",
            description="If set, this represents the .metadata.generation that the condition was\nset based upon.\nFor instance, if .metadata.generation is currently 12, but the\n.status.condition[x].observedGeneration is 9, the condition is out of date\nwith respect to the current state of the Issuer.",
        ),
    ] = None
    reason: Annotated[
        Optional[str],
        Field(
            description="Reason is a brief machine readable explanation for the condition's last\ntransition."
        ),
    ] = None
    status: Annotated[
        Literal["True", "False", "Unknown"],
        Field(description="Status of the condition, one of (`True`, `False`, `Unknown`)."),
    ]
    type: Annotated[str, Field(description="Type of the condition, known values are (`Ready`).")]


class ClusterIssuerStatus(BaseModel):
    acme: Annotated[
        Optional[AcmeModel],
        Field(
            description="ACME specific status options.\nThis field should only be set if the Issuer is configured to use an ACME\nserver to issue certificates."
        ),
    ] = None
    conditions: Annotated[
        Optional[List[IssuerCondition]],
        Field(
            description="List of status conditions to indicate the status of a CertificateRequest.\nKnown condition types are `Ready`."
        ),
    ] = None


class KubernetesModel1(BaseModel):
    service_account_ref: Annotated[
        ServiceAccountRef,
        Field(
            alias="serviceAccountRef",
            description='A reference to a service account that will be used to request a bound\ntoken (also known as "projected token"). To use this field, you must\nconfigure an RBAC rule to let cert-manager request a token.',
        ),
    ]


class AuthModel1(BaseModel):
    kubernetes: Annotated[
        KubernetesModel1,
        Field(
            description="Kubernetes authenticates with Route53 using AssumeRoleWithWebIdentity\nby passing a bound ServiceAccount token."
        ),
    ]


class KubernetesModel2(BaseModel):
    mount_path: Annotated[
        Optional[str],
        Field(
            alias="mountPath",
            description='The Vault mountPath here is the mount path to use when authenticating with\nVault. For example, setting a value to `/v1/auth/foo`, will use the path\n`/v1/auth/foo/login` to authenticate with Vault. If unspecified, the\ndefault value "/v1/auth/kubernetes" will be used.',
        ),
    ] = None
    role: Annotated[
        str,
        Field(
            description="A required field containing the Vault Role to assume. A Role binds a\nKubernetes ServiceAccount with a set of Vault policies."
        ),
    ]
    secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="secretRef",
            description="The required Secret field containing a Kubernetes ServiceAccount JWT used\nfor authenticating with Vault. Use of 'ambient credentials' is not\nsupported.",
        ),
    ] = None
    service_account_ref: Annotated[
        Optional[ServiceAccountRefModel],
        Field(
            alias="serviceAccountRef",
            description='A reference to a service account that will be used to request a bound\ntoken (also known as "projected token"). Compared to using "secretRef",\nusing this field means that you don\'t rely on statically bound tokens. To\nuse this field, you must configure an RBAC rule to let cert-manager\nrequest a token.',
        ),
    ] = None


class AuthModel2(BaseModel):
    app_role: Annotated[
        Optional[AppRole],
        Field(
            alias="appRole",
            description="AppRole authenticates with Vault using the App Role auth mechanism,\nwith the role and secret stored in a Kubernetes Secret resource.",
        ),
    ] = None
    client_certificate: Annotated[
        Optional[ClientCertificate],
        Field(
            alias="clientCertificate",
            description="ClientCertificate authenticates with Vault by presenting a client\ncertificate during the request's TLS handshake.\nWorks only when using HTTPS protocol.",
        ),
    ] = None
    kubernetes: Annotated[
        Optional[KubernetesModel2],
        Field(
            description="Kubernetes authenticates with Vault by passing the ServiceAccount\ntoken stored in the named Secret resource to the Vault server."
        ),
    ] = None
    token_secret_ref: Annotated[
        Optional[SecretRef],
        Field(
            alias="tokenSecretRef",
            description="TokenSecretRef authenticates with Vault by presenting a token.",
        ),
    ] = None


class IssuerSpec(BaseModel):
    acme: Annotated[
        Optional[Acme],
        Field(
            description="ACME configures this issuer to communicate with a RFC8555 (ACME) server\nto obtain signed x509 certificates."
        ),
    ] = None
    ca: Annotated[
        Optional[Ca],
        Field(
            description="CA configures this issuer to sign certificates using a signing CA keypair\nstored in a Secret resource.\nThis is used to build internal PKIs that are managed by cert-manager."
        ),
    ] = None
    self_signed: Annotated[
        Optional[SelfSigned],
        Field(
            alias="selfSigned",
            description="SelfSigned configures this issuer to 'self sign' certificates using the\nprivate key used to create the CertificateRequest object.",
        ),
    ] = None
    vault: Annotated[
        Optional[Vault],
        Field(
            description="Vault configures this issuer to sign certificates using a HashiCorp Vault\nPKI backend."
        ),
    ] = None
    venafi: Annotated[
        Optional[Venafi],
        Field(
            description="Venafi configures this issuer to sign certificates using a Venafi TPP\nor Venafi Cloud policy zone."
        ),
    ] = None


class IssuerStatus(BaseModel):
    acme: Annotated[
        Optional[AcmeModel],
        Field(
            description="ACME specific status options.\nThis field should only be set if the Issuer is configured to use an ACME\nserver to issue certificates."
        ),
    ] = None
    conditions: Annotated[
        Optional[List[IssuerCondition]],
        Field(
            description="List of status conditions to indicate the status of a CertificateRequest.\nKnown condition types are `Ready`."
        ),
    ] = None


class CertificateRequest(Resource):
    api_version: Annotated[
        Optional[Literal["cert-manager.io/v1"]],
        Field(
            alias="apiVersion",
            description="APIVersion defines the versioned schema of this representation of an object.\nServers should convert recognized schemas to the latest internal value, and\nmay reject unrecognized values.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",
        ),
    ] = "cert-manager.io/v1"
    kind: Annotated[
        Optional[Literal["CertificateRequest"]],
        Field(
            description="Kind is a string value representing the REST resource this object represents.\nServers may infer this from the endpoint the client submits requests to.\nCannot be updated.\nIn CamelCase.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    ] = "CertificateRequest"
    metadata: Optional[apimachinery.ObjectMeta] = None
    spec: Optional[CertificateRequestSpec] = None
    status: Optional[CertificateRequestStatus] = None


class Certificate(Resource):
    api_version: Annotated[
        Optional[Literal["cert-manager.io/v1"]],
        Field(
            alias="apiVersion",
            description="APIVersion defines the versioned schema of this representation of an object.\nServers should convert recognized schemas to the latest internal value, and\nmay reject unrecognized values.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",
        ),
    ] = "cert-manager.io/v1"
    kind: Annotated[
        Optional[Literal["Certificate"]],
        Field(
            description="Kind is a string value representing the REST resource this object represents.\nServers may infer this from the endpoint the client submits requests to.\nCannot be updated.\nIn CamelCase.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    ] = "Certificate"
    metadata: Optional[apimachinery.ObjectMeta] = None
    spec: Optional[CertificateSpec] = None
    status: Optional[CertificateStatus] = None


class ClusterIssuer(Resource):
    api_version: Annotated[
        Optional[Literal["cert-manager.io/v1"]],
        Field(
            alias="apiVersion",
            description="APIVersion defines the versioned schema of this representation of an object.\nServers should convert recognized schemas to the latest internal value, and\nmay reject unrecognized values.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",
        ),
    ] = "cert-manager.io/v1"
    kind: Annotated[
        Optional[Literal["ClusterIssuer"]],
        Field(
            description="Kind is a string value representing the REST resource this object represents.\nServers may infer this from the endpoint the client submits requests to.\nCannot be updated.\nIn CamelCase.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    ] = "ClusterIssuer"
    metadata: Optional[apimachinery.ObjectMeta] = None
    spec: ClusterIssuerSpec
    status: Optional[ClusterIssuerStatus] = None


class Issuer(Resource):
    api_version: Annotated[
        Optional[Literal["cert-manager.io/v1"]],
        Field(
            alias="apiVersion",
            description="APIVersion defines the versioned schema of this representation of an object.\nServers should convert recognized schemas to the latest internal value, and\nmay reject unrecognized values.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources",
        ),
    ] = "cert-manager.io/v1"
    kind: Annotated[
        Optional[Literal["Issuer"]],
        Field(
            description="Kind is a string value representing the REST resource this object represents.\nServers may infer this from the endpoint the client submits requests to.\nCannot be updated.\nIn CamelCase.\nMore info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
        ),
    ] = "Issuer"
    metadata: Optional[apimachinery.ObjectMeta] = None
    spec: IssuerSpec
    status: Optional[IssuerStatus] = None
