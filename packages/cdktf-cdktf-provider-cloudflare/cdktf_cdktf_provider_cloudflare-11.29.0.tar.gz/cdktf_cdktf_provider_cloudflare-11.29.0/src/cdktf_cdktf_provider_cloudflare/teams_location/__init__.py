r'''
# `cloudflare_teams_location`

Refer to the Terraform Registry for docs: [`cloudflare_teams_location`](https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class TeamsLocation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocation",
):
    '''Represents a {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location cloudflare_teams_location}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        name: builtins.str,
        client_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dns_destination_ips_id: typing.Optional[builtins.str] = None,
        dns_destination_ipv6_block_id: typing.Optional[builtins.str] = None,
        ecs_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoints: typing.Optional[typing.Union["TeamsLocationEndpoints", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TeamsLocationNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location cloudflare_teams_location} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#account_id TeamsLocation#account_id}
        :param name: Name of the teams location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#name TeamsLocation#name}
        :param client_default: Indicator that this is the default location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#client_default TeamsLocation#client_default}
        :param dns_destination_ips_id: IPv4 binding assigned to this location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#dns_destination_ips_id TeamsLocation#dns_destination_ips_id}
        :param dns_destination_ipv6_block_id: IPv6 block binding assigned to this location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#dns_destination_ipv6_block_id TeamsLocation#dns_destination_ipv6_block_id}
        :param ecs_support: Indicator that this location needs to resolve EDNS queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#ecs_support TeamsLocation#ecs_support}
        :param endpoints: endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#endpoints TeamsLocation#endpoints}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#id TeamsLocation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param networks: The networks CIDRs that comprise the location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7462c0fcd7ebd034abd34575d8868b9859e4f73cb2bf3e858986daa565718aee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = TeamsLocationConfig(
            account_id=account_id,
            name=name,
            client_default=client_default,
            dns_destination_ips_id=dns_destination_ips_id,
            dns_destination_ipv6_block_id=dns_destination_ipv6_block_id,
            ecs_support=ecs_support,
            endpoints=endpoints,
            id=id,
            networks=networks,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a TeamsLocation resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the TeamsLocation to import.
        :param import_from_id: The id of the existing TeamsLocation that should be imported. Refer to the {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the TeamsLocation to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7927a62c38279c8d3152d5703cb39c03534f15c0d3f967dfadf52e39796fbf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEndpoints")
    def put_endpoints(
        self,
        *,
        doh: typing.Optional[typing.Union["TeamsLocationEndpointsDoh", typing.Dict[builtins.str, typing.Any]]] = None,
        dot: typing.Optional[typing.Union["TeamsLocationEndpointsDot", typing.Dict[builtins.str, typing.Any]]] = None,
        ipv4: typing.Optional[typing.Union["TeamsLocationEndpointsIpv4", typing.Dict[builtins.str, typing.Any]]] = None,
        ipv6: typing.Optional[typing.Union["TeamsLocationEndpointsIpv6", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param doh: doh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#doh TeamsLocation#doh}
        :param dot: dot block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#dot TeamsLocation#dot}
        :param ipv4: ipv4 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#ipv4 TeamsLocation#ipv4}
        :param ipv6: ipv6 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#ipv6 TeamsLocation#ipv6}
        '''
        value = TeamsLocationEndpoints(doh=doh, dot=dot, ipv4=ipv4, ipv6=ipv6)

        return typing.cast(None, jsii.invoke(self, "putEndpoints", [value]))

    @jsii.member(jsii_name="putNetworks")
    def put_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TeamsLocationNetworks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a08ff13b8e9ff642bd681f3b6ff244a1b4314fc78170625541cc2b3a956a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworks", [value]))

    @jsii.member(jsii_name="resetClientDefault")
    def reset_client_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientDefault", []))

    @jsii.member(jsii_name="resetDnsDestinationIpsId")
    def reset_dns_destination_ips_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsDestinationIpsId", []))

    @jsii.member(jsii_name="resetDnsDestinationIpv6BlockId")
    def reset_dns_destination_ipv6_block_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsDestinationIpv6BlockId", []))

    @jsii.member(jsii_name="resetEcsSupport")
    def reset_ecs_support(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEcsSupport", []))

    @jsii.member(jsii_name="resetEndpoints")
    def reset_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoints", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNetworks")
    def reset_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworks", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="anonymizedLogsEnabled")
    def anonymized_logs_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "anonymizedLogsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="dohSubdomain")
    def doh_subdomain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dohSubdomain"))

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> "TeamsLocationEndpointsOutputReference":
        return typing.cast("TeamsLocationEndpointsOutputReference", jsii.get(self, "endpoints"))

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @builtins.property
    @jsii.member(jsii_name="ipv4Destination")
    def ipv4_destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Destination"))

    @builtins.property
    @jsii.member(jsii_name="ipv4DestinationBackup")
    def ipv4_destination_backup(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4DestinationBackup"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> "TeamsLocationNetworksList":
        return typing.cast("TeamsLocationNetworksList", jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientDefaultInput")
    def client_default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsDestinationIpsIdInput")
    def dns_destination_ips_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsDestinationIpsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsDestinationIpv6BlockIdInput")
    def dns_destination_ipv6_block_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsDestinationIpv6BlockIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ecsSupportInput")
    def ecs_support_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ecsSupportInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointsInput")
    def endpoints_input(self) -> typing.Optional["TeamsLocationEndpoints"]:
        return typing.cast(typing.Optional["TeamsLocationEndpoints"], jsii.get(self, "endpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networksInput")
    def networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TeamsLocationNetworks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TeamsLocationNetworks"]]], jsii.get(self, "networksInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d07f09079b077bd18700fc2b15419d0fbf6f2871bd171b256554b259c1a8ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientDefault")
    def client_default(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientDefault"))

    @client_default.setter
    def client_default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f73c3e8c1053664dd8118c6fec081862991a41b28eb385b7a5ee5d11e17d14b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsDestinationIpsId")
    def dns_destination_ips_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsDestinationIpsId"))

    @dns_destination_ips_id.setter
    def dns_destination_ips_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a620ef97b2f2f264926619c36ae7ce94fa400654b9fa51846954ace23e4876c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsDestinationIpsId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsDestinationIpv6BlockId")
    def dns_destination_ipv6_block_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsDestinationIpv6BlockId"))

    @dns_destination_ipv6_block_id.setter
    def dns_destination_ipv6_block_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ed83d42d9acf689bed83cbeca52e66b3f76ed2f0cd5440c9cedf7821893a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsDestinationIpv6BlockId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ecsSupport")
    def ecs_support(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ecsSupport"))

    @ecs_support.setter
    def ecs_support(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61a9b8c4c78514a6a0210a23cf02e3d09d58096dfd9d13b4f192b51294f7a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ecsSupport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e28f8281a4edca1314b4339bf3d944dbb9e38f2b511956ca6900930d100bc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__867aae351ba1f00d1a6d5a2d1c14ef23b24fd93397d65c27d58b50b34a9aef74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_id": "accountId",
        "name": "name",
        "client_default": "clientDefault",
        "dns_destination_ips_id": "dnsDestinationIpsId",
        "dns_destination_ipv6_block_id": "dnsDestinationIpv6BlockId",
        "ecs_support": "ecsSupport",
        "endpoints": "endpoints",
        "id": "id",
        "networks": "networks",
    },
)
class TeamsLocationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        account_id: builtins.str,
        name: builtins.str,
        client_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dns_destination_ips_id: typing.Optional[builtins.str] = None,
        dns_destination_ipv6_block_id: typing.Optional[builtins.str] = None,
        ecs_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        endpoints: typing.Optional[typing.Union["TeamsLocationEndpoints", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TeamsLocationNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#account_id TeamsLocation#account_id}
        :param name: Name of the teams location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#name TeamsLocation#name}
        :param client_default: Indicator that this is the default location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#client_default TeamsLocation#client_default}
        :param dns_destination_ips_id: IPv4 binding assigned to this location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#dns_destination_ips_id TeamsLocation#dns_destination_ips_id}
        :param dns_destination_ipv6_block_id: IPv6 block binding assigned to this location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#dns_destination_ipv6_block_id TeamsLocation#dns_destination_ipv6_block_id}
        :param ecs_support: Indicator that this location needs to resolve EDNS queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#ecs_support TeamsLocation#ecs_support}
        :param endpoints: endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#endpoints TeamsLocation#endpoints}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#id TeamsLocation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param networks: The networks CIDRs that comprise the location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(endpoints, dict):
            endpoints = TeamsLocationEndpoints(**endpoints)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf637fdfe4c2e340899c8690c64d3284b321fdde1b1b6bddb2524d948cf6be6a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument client_default", value=client_default, expected_type=type_hints["client_default"])
            check_type(argname="argument dns_destination_ips_id", value=dns_destination_ips_id, expected_type=type_hints["dns_destination_ips_id"])
            check_type(argname="argument dns_destination_ipv6_block_id", value=dns_destination_ipv6_block_id, expected_type=type_hints["dns_destination_ipv6_block_id"])
            check_type(argname="argument ecs_support", value=ecs_support, expected_type=type_hints["ecs_support"])
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if client_default is not None:
            self._values["client_default"] = client_default
        if dns_destination_ips_id is not None:
            self._values["dns_destination_ips_id"] = dns_destination_ips_id
        if dns_destination_ipv6_block_id is not None:
            self._values["dns_destination_ipv6_block_id"] = dns_destination_ipv6_block_id
        if ecs_support is not None:
            self._values["ecs_support"] = ecs_support
        if endpoints is not None:
            self._values["endpoints"] = endpoints
        if id is not None:
            self._values["id"] = id
        if networks is not None:
            self._values["networks"] = networks

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def account_id(self) -> builtins.str:
        '''The account identifier to target for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#account_id TeamsLocation#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the teams location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#name TeamsLocation#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicator that this is the default location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#client_default TeamsLocation#client_default}
        '''
        result = self._values.get("client_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dns_destination_ips_id(self) -> typing.Optional[builtins.str]:
        '''IPv4 binding assigned to this location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#dns_destination_ips_id TeamsLocation#dns_destination_ips_id}
        '''
        result = self._values.get("dns_destination_ips_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_destination_ipv6_block_id(self) -> typing.Optional[builtins.str]:
        '''IPv6 block binding assigned to this location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#dns_destination_ipv6_block_id TeamsLocation#dns_destination_ipv6_block_id}
        '''
        result = self._values.get("dns_destination_ipv6_block_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ecs_support(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicator that this location needs to resolve EDNS queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#ecs_support TeamsLocation#ecs_support}
        '''
        result = self._values.get("ecs_support")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def endpoints(self) -> typing.Optional["TeamsLocationEndpoints"]:
        '''endpoints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#endpoints TeamsLocation#endpoints}
        '''
        result = self._values.get("endpoints")
        return typing.cast(typing.Optional["TeamsLocationEndpoints"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#id TeamsLocation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TeamsLocationNetworks"]]]:
        '''The networks CIDRs that comprise the location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}
        '''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TeamsLocationNetworks"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsLocationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpoints",
    jsii_struct_bases=[],
    name_mapping={"doh": "doh", "dot": "dot", "ipv4": "ipv4", "ipv6": "ipv6"},
)
class TeamsLocationEndpoints:
    def __init__(
        self,
        *,
        doh: typing.Optional[typing.Union["TeamsLocationEndpointsDoh", typing.Dict[builtins.str, typing.Any]]] = None,
        dot: typing.Optional[typing.Union["TeamsLocationEndpointsDot", typing.Dict[builtins.str, typing.Any]]] = None,
        ipv4: typing.Optional[typing.Union["TeamsLocationEndpointsIpv4", typing.Dict[builtins.str, typing.Any]]] = None,
        ipv6: typing.Optional[typing.Union["TeamsLocationEndpointsIpv6", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param doh: doh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#doh TeamsLocation#doh}
        :param dot: dot block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#dot TeamsLocation#dot}
        :param ipv4: ipv4 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#ipv4 TeamsLocation#ipv4}
        :param ipv6: ipv6 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#ipv6 TeamsLocation#ipv6}
        '''
        if isinstance(doh, dict):
            doh = TeamsLocationEndpointsDoh(**doh)
        if isinstance(dot, dict):
            dot = TeamsLocationEndpointsDot(**dot)
        if isinstance(ipv4, dict):
            ipv4 = TeamsLocationEndpointsIpv4(**ipv4)
        if isinstance(ipv6, dict):
            ipv6 = TeamsLocationEndpointsIpv6(**ipv6)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__405ad6f2a2bd67544bfb8fbe45b1e966a0bc784a7e141916509b9c7fc624efbe)
            check_type(argname="argument doh", value=doh, expected_type=type_hints["doh"])
            check_type(argname="argument dot", value=dot, expected_type=type_hints["dot"])
            check_type(argname="argument ipv4", value=ipv4, expected_type=type_hints["ipv4"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if doh is not None:
            self._values["doh"] = doh
        if dot is not None:
            self._values["dot"] = dot
        if ipv4 is not None:
            self._values["ipv4"] = ipv4
        if ipv6 is not None:
            self._values["ipv6"] = ipv6

    @builtins.property
    def doh(self) -> typing.Optional["TeamsLocationEndpointsDoh"]:
        '''doh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#doh TeamsLocation#doh}
        '''
        result = self._values.get("doh")
        return typing.cast(typing.Optional["TeamsLocationEndpointsDoh"], result)

    @builtins.property
    def dot(self) -> typing.Optional["TeamsLocationEndpointsDot"]:
        '''dot block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#dot TeamsLocation#dot}
        '''
        result = self._values.get("dot")
        return typing.cast(typing.Optional["TeamsLocationEndpointsDot"], result)

    @builtins.property
    def ipv4(self) -> typing.Optional["TeamsLocationEndpointsIpv4"]:
        '''ipv4 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#ipv4 TeamsLocation#ipv4}
        '''
        result = self._values.get("ipv4")
        return typing.cast(typing.Optional["TeamsLocationEndpointsIpv4"], result)

    @builtins.property
    def ipv6(self) -> typing.Optional["TeamsLocationEndpointsIpv6"]:
        '''ipv6 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#ipv6 TeamsLocation#ipv6}
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional["TeamsLocationEndpointsIpv6"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsLocationEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsDoh",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "networks": "networks"},
)
class TeamsLocationEndpointsDoh:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TeamsLocationEndpointsDohNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.
        :param networks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a53afaf3399bbf316c3f0fe61b53619b763d1fb2d66cc265ba6e9f220037c6ad)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if networks is not None:
            self._values["networks"] = networks

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TeamsLocationEndpointsDohNetworks"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}.'''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TeamsLocationEndpointsDohNetworks"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsLocationEndpointsDoh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsDohNetworks",
    jsii_struct_bases=[],
    name_mapping={"network": "network"},
)
class TeamsLocationEndpointsDohNetworks:
    def __init__(self, *, network: typing.Optional[builtins.str] = None) -> None:
        '''
        :param network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#network TeamsLocation#network}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ccbbb9d4f33bd356604758706cf3863daa9d6d5f1797ce3dfe5e7e464b78796)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network is not None:
            self._values["network"] = network

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#network TeamsLocation#network}.'''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsLocationEndpointsDohNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsLocationEndpointsDohNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsDohNetworksList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe2eb5f16743a7bb2d26af3c2f81c83b99e390cc1d48cd7829e954846bf8d8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TeamsLocationEndpointsDohNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db802458cbf0cbba335fb8568f5b40fb6c314c81c107da0a6d3102ceb76a66ea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TeamsLocationEndpointsDohNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3be9def5719d905af698491eed4fcc8f3d8469d37d7778f02d1f6fc4ebc6d35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3c3df9268cde4713db8274b40b9598b350d50dba01bdb5557dad9440ba37dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa312a5ffdf1ec45dda8375414f1338c048f82ffd5d573f3270b20ced65e882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDohNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDohNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDohNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a03e4695eb727fc538f1874ce8bf3cb08fbfd9c1f3848b0cede44f30e345a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TeamsLocationEndpointsDohNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsDohNetworksOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8737a5a3df42797b2092e2c91a17cb2677636a8a5ce035e69b09d9d3b49cac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be7011f5a8f8d63335427819084b33081512b15412a75a3c2cf9fa4e088683b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsDohNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsDohNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsDohNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d6ee787de954181e0ae165e9219f33b6e64816d4b5886a68e7686996dc25f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TeamsLocationEndpointsDohOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsDohOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369f28c414c6e4f84e05ee92827b40e093b36e5eb0c5b7dc99eb979029e0016c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworks")
    def put_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsDohNetworks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e18e1f827b9a66969258d229c562ea0bbb38cbd19a1929569690284183ecf5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworks", [value]))

    @jsii.member(jsii_name="resetNetworks")
    def reset_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworks", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationEnabled")
    def authentication_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "authenticationEnabled"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> TeamsLocationEndpointsDohNetworksList:
        return typing.cast(TeamsLocationEndpointsDohNetworksList, jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="requireToken")
    def require_token(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "requireToken"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="networksInput")
    def networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDohNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDohNetworks]]], jsii.get(self, "networksInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0634e10e9cdf638fe5564e5097520a19138040ebd7184cd02a961bd5d8df81bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsLocationEndpointsDoh]:
        return typing.cast(typing.Optional[TeamsLocationEndpointsDoh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsLocationEndpointsDoh]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fe3e5fb9f0b581ca3bc83229cadf85e161cfb85765b94f10ae67f9a0836633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsDot",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "networks": "networks"},
)
class TeamsLocationEndpointsDot:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TeamsLocationEndpointsDotNetworks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.
        :param networks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87296bee4d846468612c58d8b4897fc3f803498a93653e25a2bb4db8019acd93)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if networks is not None:
            self._values["networks"] = networks

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TeamsLocationEndpointsDotNetworks"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}.'''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TeamsLocationEndpointsDotNetworks"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsLocationEndpointsDot(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsDotNetworks",
    jsii_struct_bases=[],
    name_mapping={"network": "network"},
)
class TeamsLocationEndpointsDotNetworks:
    def __init__(self, *, network: typing.Optional[builtins.str] = None) -> None:
        '''
        :param network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#network TeamsLocation#network}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb6fb1109ab12a732e98624396387cf07f54ecacf95d7b71c68e74503495604)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network is not None:
            self._values["network"] = network

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#network TeamsLocation#network}.'''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsLocationEndpointsDotNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsLocationEndpointsDotNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsDotNetworksList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f04745ae7f3010cd28ee6926509aa0be36f5c24dc1e9fcb3a01c8d3bce14e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TeamsLocationEndpointsDotNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2878de1078fd9d140c81d5ce5faae5a5c19dacbcf00d2000f174d9fabd54d79b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TeamsLocationEndpointsDotNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b92273ccc90694817797ab11027dd069caaf339f203960dfc230ea9edadfbfda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45199bafe49c684b571fd989ff05acd866188839c79ef1a526dc7d6f4bbe5440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26d6fea80a0012e31745f4fbd41a349358e33bd06a4fa94b8544e62e5924483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDotNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDotNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDotNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d323e4fc31c021ed4aa893cfda96d84da5da2841f2e7f467fe3eacaaca7a20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TeamsLocationEndpointsDotNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsDotNetworksOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5594627fb39ae6c7bd8b57a9d4796e81781fa4e9d86c0e928dc3a1babc1a0c40)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33b541e948ccd35770dbeae34db81e7a02abd27880205abf137f5d54e1b5222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsDotNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsDotNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsDotNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1c7bcdf31e7df8d9a74815ee81ae97a7f11cdb2b6d92c911995d3786d2d5c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TeamsLocationEndpointsDotOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsDotOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87392312e5126b15cdfbc2a9954e2ccd1ad5a76895e4f201d38ba1b270184e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworks")
    def put_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsDotNetworks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6feeca862dd6ed4020d14efcc59b37295104aa450259d40ce91738e62f87607d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworks", [value]))

    @jsii.member(jsii_name="resetNetworks")
    def reset_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworks", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationEnabled")
    def authentication_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "authenticationEnabled"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> TeamsLocationEndpointsDotNetworksList:
        return typing.cast(TeamsLocationEndpointsDotNetworksList, jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="requireToken")
    def require_token(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "requireToken"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="networksInput")
    def networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDotNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDotNetworks]]], jsii.get(self, "networksInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e817f8a91f992b515ef1742cce88309f2f32b7f10861c9918a38427608c2940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsLocationEndpointsDot]:
        return typing.cast(typing.Optional[TeamsLocationEndpointsDot], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsLocationEndpointsDot]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cac9bc7c649673e6f49417e43a18fced3ed21cc814186692c9c21973bd1bd41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsIpv4",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class TeamsLocationEndpointsIpv4:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f975412f2fd57af9064a053a77baf6b52b080cddc3633fb93b44982445684426)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsLocationEndpointsIpv4(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsLocationEndpointsIpv4OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsIpv4OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ffe42f83e5a999f9931b68c11e787e553e29586cb1fc9b5e53ed18cb4b1109)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="authenticationEnabled")
    def authentication_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "authenticationEnabled"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e86cb3cd5b20334762d0fed93e7bed947743e69827e3d5c569faa36b43f9f1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsLocationEndpointsIpv4]:
        return typing.cast(typing.Optional[TeamsLocationEndpointsIpv4], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsLocationEndpointsIpv4],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849034eab0ef8f0e9dc58c8040e3c3e68805b1d38718d198b9f2256bc8264e99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsIpv6",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "networks": "networks"},
)
class TeamsLocationEndpointsIpv6:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TeamsLocationEndpointsIpv6Networks", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.
        :param networks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2640b35b7873e07c662dbccdd83e270ac611dcc4f774bc8025564da1eaf654f4)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument networks", value=networks, expected_type=type_hints["networks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if networks is not None:
            self._values["networks"] = networks

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def networks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TeamsLocationEndpointsIpv6Networks"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}.'''
        result = self._values.get("networks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TeamsLocationEndpointsIpv6Networks"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsLocationEndpointsIpv6(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsIpv6Networks",
    jsii_struct_bases=[],
    name_mapping={"network": "network"},
)
class TeamsLocationEndpointsIpv6Networks:
    def __init__(self, *, network: typing.Optional[builtins.str] = None) -> None:
        '''
        :param network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#network TeamsLocation#network}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7958f8df7d0a929a33ecd6ba03ef94464a086657e9b635e5de41b83bd5659c9)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network is not None:
            self._values["network"] = network

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#network TeamsLocation#network}.'''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsLocationEndpointsIpv6Networks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsLocationEndpointsIpv6NetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsIpv6NetworksList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49cb877245be38aa209f769176875c83971862fafd94cf4e6464183eb367b6fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TeamsLocationEndpointsIpv6NetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68d7a5a2b0012103b03d13c031fe34b58cda0b5668083906f2ee06d271d0e86)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TeamsLocationEndpointsIpv6NetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006b3485263ca290a2313fd6857da44b08c1b4213bd794e8bcf61017d16678ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb0c5e4760782627ef74d260d623c00fe8fb5cd7b0652388db4833adc1c82d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf7469c5299f63db89e3d5ccd9528b4a7c82406693283c8470fa9e618bcc1ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsIpv6Networks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsIpv6Networks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsIpv6Networks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c51d3fb7bff81a30f973886c7a2ab90e14d74b4cc160e0c1f8b14c0494e086b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TeamsLocationEndpointsIpv6NetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsIpv6NetworksOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68379f8d4942e5679c83a9dbe6c7a88b6f5c647f102a08400322020e361856c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08367eab72669c7c06c90643650248cb0ee7e7caa62c711b91f0411478c1c19c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsIpv6Networks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsIpv6Networks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsIpv6Networks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f20e4f26b40cbe8a6af84c3b01b8b9cd9225588c4de1c974884eb5abea8f9b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TeamsLocationEndpointsIpv6OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsIpv6OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422308ad23ff41661760b53a8186c7ad30c33e18ca51bd7a3d87187e8ae4be0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworks")
    def put_networks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsIpv6Networks, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2abf56686cffb006b4c464645b81601b1cb0a66cff96262e2787c71bff7e284f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworks", [value]))

    @jsii.member(jsii_name="resetNetworks")
    def reset_networks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworks", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationEnabled")
    def authentication_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "authenticationEnabled"))

    @builtins.property
    @jsii.member(jsii_name="networks")
    def networks(self) -> TeamsLocationEndpointsIpv6NetworksList:
        return typing.cast(TeamsLocationEndpointsIpv6NetworksList, jsii.get(self, "networks"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="networksInput")
    def networks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsIpv6Networks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsIpv6Networks]]], jsii.get(self, "networksInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09be9738a22d05fd63c84b2f08c81283339bd8eb27eae5f2f315d91e42f4e0da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsLocationEndpointsIpv6]:
        return typing.cast(typing.Optional[TeamsLocationEndpointsIpv6], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TeamsLocationEndpointsIpv6],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abcb1c6f467ee0edc6ccd04c5bbeed123f04de8a53e209abf695e8cb7a19f4c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TeamsLocationEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationEndpointsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a08354d562a024fb28f1d3f9f8f74cf1b3245732b254e6f187d227d0ee97de0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDoh")
    def put_doh(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsDohNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.
        :param networks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}.
        '''
        value = TeamsLocationEndpointsDoh(enabled=enabled, networks=networks)

        return typing.cast(None, jsii.invoke(self, "putDoh", [value]))

    @jsii.member(jsii_name="putDot")
    def put_dot(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsDotNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.
        :param networks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}.
        '''
        value = TeamsLocationEndpointsDot(enabled=enabled, networks=networks)

        return typing.cast(None, jsii.invoke(self, "putDot", [value]))

    @jsii.member(jsii_name="putIpv4")
    def put_ipv4(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.
        '''
        value = TeamsLocationEndpointsIpv4(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putIpv4", [value]))

    @jsii.member(jsii_name="putIpv6")
    def put_ipv6(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsIpv6Networks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#enabled TeamsLocation#enabled}.
        :param networks: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#networks TeamsLocation#networks}.
        '''
        value = TeamsLocationEndpointsIpv6(enabled=enabled, networks=networks)

        return typing.cast(None, jsii.invoke(self, "putIpv6", [value]))

    @jsii.member(jsii_name="resetDoh")
    def reset_doh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDoh", []))

    @jsii.member(jsii_name="resetDot")
    def reset_dot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDot", []))

    @jsii.member(jsii_name="resetIpv4")
    def reset_ipv4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4", []))

    @jsii.member(jsii_name="resetIpv6")
    def reset_ipv6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6", []))

    @builtins.property
    @jsii.member(jsii_name="doh")
    def doh(self) -> TeamsLocationEndpointsDohOutputReference:
        return typing.cast(TeamsLocationEndpointsDohOutputReference, jsii.get(self, "doh"))

    @builtins.property
    @jsii.member(jsii_name="dot")
    def dot(self) -> TeamsLocationEndpointsDotOutputReference:
        return typing.cast(TeamsLocationEndpointsDotOutputReference, jsii.get(self, "dot"))

    @builtins.property
    @jsii.member(jsii_name="ipv4")
    def ipv4(self) -> TeamsLocationEndpointsIpv4OutputReference:
        return typing.cast(TeamsLocationEndpointsIpv4OutputReference, jsii.get(self, "ipv4"))

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> TeamsLocationEndpointsIpv6OutputReference:
        return typing.cast(TeamsLocationEndpointsIpv6OutputReference, jsii.get(self, "ipv6"))

    @builtins.property
    @jsii.member(jsii_name="dohInput")
    def doh_input(self) -> typing.Optional[TeamsLocationEndpointsDoh]:
        return typing.cast(typing.Optional[TeamsLocationEndpointsDoh], jsii.get(self, "dohInput"))

    @builtins.property
    @jsii.member(jsii_name="dotInput")
    def dot_input(self) -> typing.Optional[TeamsLocationEndpointsDot]:
        return typing.cast(typing.Optional[TeamsLocationEndpointsDot], jsii.get(self, "dotInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4Input")
    def ipv4_input(self) -> typing.Optional[TeamsLocationEndpointsIpv4]:
        return typing.cast(typing.Optional[TeamsLocationEndpointsIpv4], jsii.get(self, "ipv4Input"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Input")
    def ipv6_input(self) -> typing.Optional[TeamsLocationEndpointsIpv6]:
        return typing.cast(typing.Optional[TeamsLocationEndpointsIpv6], jsii.get(self, "ipv6Input"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TeamsLocationEndpoints]:
        return typing.cast(typing.Optional[TeamsLocationEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TeamsLocationEndpoints]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1087c877a7d4e10434ec78e808d8f354f793da13ed5f2461127d42c8d64cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationNetworks",
    jsii_struct_bases=[],
    name_mapping={"network": "network"},
)
class TeamsLocationNetworks:
    def __init__(self, *, network: typing.Optional[builtins.str] = None) -> None:
        '''
        :param network: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#network TeamsLocation#network}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119298ce4f1f5f2ee974235314ad6a44be7dbd1e03653c41eff32095695b7063)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network is not None:
            self._values["network"] = network

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/cloudflare/cloudflare/4.51.0/docs/resources/teams_location#network TeamsLocation#network}.'''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TeamsLocationNetworks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TeamsLocationNetworksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationNetworksList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4633e12d4db1c02144181f742e66a4d7b1b43f49c3fbd3c9f4fe0e62518887ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TeamsLocationNetworksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e01cebb75bccd7fba0eb901d5d23069e3af44dc4f51a94bd42f2b3541fd779)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TeamsLocationNetworksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b06c0325d260d7fa6a93961088691afee5aeeb4350cd96e7867592684fd2036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f791d6b48489de48161c3ac50ccda88d65fef6689b213633fb4122e21e7436d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976d5af6336e435d08000145df43747402ad1655c353380f8f165d67e4169141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationNetworks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationNetworks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationNetworks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b21fd78987a2675fb766f37b3bfbd527f93b770475319d4da367e1f8a76e76a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class TeamsLocationNetworksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.teamsLocation.TeamsLocationNetworksOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21eb7ae4952afcc3048e399457e2202645a763f2edf5acca3cb121dadf41afcd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74629982ab28d987e2095f81cbbd2348962076b71f8d2e7b12383956dc336ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationNetworks]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationNetworks]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationNetworks]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea7ba25821cec48d0cc47723f962462657010c4faff98ad2cf66695d8d4ebce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "TeamsLocation",
    "TeamsLocationConfig",
    "TeamsLocationEndpoints",
    "TeamsLocationEndpointsDoh",
    "TeamsLocationEndpointsDohNetworks",
    "TeamsLocationEndpointsDohNetworksList",
    "TeamsLocationEndpointsDohNetworksOutputReference",
    "TeamsLocationEndpointsDohOutputReference",
    "TeamsLocationEndpointsDot",
    "TeamsLocationEndpointsDotNetworks",
    "TeamsLocationEndpointsDotNetworksList",
    "TeamsLocationEndpointsDotNetworksOutputReference",
    "TeamsLocationEndpointsDotOutputReference",
    "TeamsLocationEndpointsIpv4",
    "TeamsLocationEndpointsIpv4OutputReference",
    "TeamsLocationEndpointsIpv6",
    "TeamsLocationEndpointsIpv6Networks",
    "TeamsLocationEndpointsIpv6NetworksList",
    "TeamsLocationEndpointsIpv6NetworksOutputReference",
    "TeamsLocationEndpointsIpv6OutputReference",
    "TeamsLocationEndpointsOutputReference",
    "TeamsLocationNetworks",
    "TeamsLocationNetworksList",
    "TeamsLocationNetworksOutputReference",
]

publication.publish()

def _typecheckingstub__7462c0fcd7ebd034abd34575d8868b9859e4f73cb2bf3e858986daa565718aee(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    name: builtins.str,
    client_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dns_destination_ips_id: typing.Optional[builtins.str] = None,
    dns_destination_ipv6_block_id: typing.Optional[builtins.str] = None,
    ecs_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoints: typing.Optional[typing.Union[TeamsLocationEndpoints, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7927a62c38279c8d3152d5703cb39c03534f15c0d3f967dfadf52e39796fbf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a08ff13b8e9ff642bd681f3b6ff244a1b4314fc78170625541cc2b3a956a83(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d07f09079b077bd18700fc2b15419d0fbf6f2871bd171b256554b259c1a8ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f73c3e8c1053664dd8118c6fec081862991a41b28eb385b7a5ee5d11e17d14b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a620ef97b2f2f264926619c36ae7ce94fa400654b9fa51846954ace23e4876c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ed83d42d9acf689bed83cbeca52e66b3f76ed2f0cd5440c9cedf7821893a90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61a9b8c4c78514a6a0210a23cf02e3d09d58096dfd9d13b4f192b51294f7a9d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e28f8281a4edca1314b4339bf3d944dbb9e38f2b511956ca6900930d100bc20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867aae351ba1f00d1a6d5a2d1c14ef23b24fd93397d65c27d58b50b34a9aef74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf637fdfe4c2e340899c8690c64d3284b321fdde1b1b6bddb2524d948cf6be6a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    name: builtins.str,
    client_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dns_destination_ips_id: typing.Optional[builtins.str] = None,
    dns_destination_ipv6_block_id: typing.Optional[builtins.str] = None,
    ecs_support: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    endpoints: typing.Optional[typing.Union[TeamsLocationEndpoints, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__405ad6f2a2bd67544bfb8fbe45b1e966a0bc784a7e141916509b9c7fc624efbe(
    *,
    doh: typing.Optional[typing.Union[TeamsLocationEndpointsDoh, typing.Dict[builtins.str, typing.Any]]] = None,
    dot: typing.Optional[typing.Union[TeamsLocationEndpointsDot, typing.Dict[builtins.str, typing.Any]]] = None,
    ipv4: typing.Optional[typing.Union[TeamsLocationEndpointsIpv4, typing.Dict[builtins.str, typing.Any]]] = None,
    ipv6: typing.Optional[typing.Union[TeamsLocationEndpointsIpv6, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53afaf3399bbf316c3f0fe61b53619b763d1fb2d66cc265ba6e9f220037c6ad(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsDohNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ccbbb9d4f33bd356604758706cf3863daa9d6d5f1797ce3dfe5e7e464b78796(
    *,
    network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe2eb5f16743a7bb2d26af3c2f81c83b99e390cc1d48cd7829e954846bf8d8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db802458cbf0cbba335fb8568f5b40fb6c314c81c107da0a6d3102ceb76a66ea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3be9def5719d905af698491eed4fcc8f3d8469d37d7778f02d1f6fc4ebc6d35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c3df9268cde4713db8274b40b9598b350d50dba01bdb5557dad9440ba37dbd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa312a5ffdf1ec45dda8375414f1338c048f82ffd5d573f3270b20ced65e882(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a03e4695eb727fc538f1874ce8bf3cb08fbfd9c1f3848b0cede44f30e345a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDohNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8737a5a3df42797b2092e2c91a17cb2677636a8a5ce035e69b09d9d3b49cac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be7011f5a8f8d63335427819084b33081512b15412a75a3c2cf9fa4e088683b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d6ee787de954181e0ae165e9219f33b6e64816d4b5886a68e7686996dc25f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsDohNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__369f28c414c6e4f84e05ee92827b40e093b36e5eb0c5b7dc99eb979029e0016c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e18e1f827b9a66969258d229c562ea0bbb38cbd19a1929569690284183ecf5b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsDohNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0634e10e9cdf638fe5564e5097520a19138040ebd7184cd02a961bd5d8df81bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fe3e5fb9f0b581ca3bc83229cadf85e161cfb85765b94f10ae67f9a0836633(
    value: typing.Optional[TeamsLocationEndpointsDoh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87296bee4d846468612c58d8b4897fc3f803498a93653e25a2bb4db8019acd93(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsDotNetworks, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb6fb1109ab12a732e98624396387cf07f54ecacf95d7b71c68e74503495604(
    *,
    network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f04745ae7f3010cd28ee6926509aa0be36f5c24dc1e9fcb3a01c8d3bce14e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2878de1078fd9d140c81d5ce5faae5a5c19dacbcf00d2000f174d9fabd54d79b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b92273ccc90694817797ab11027dd069caaf339f203960dfc230ea9edadfbfda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45199bafe49c684b571fd989ff05acd866188839c79ef1a526dc7d6f4bbe5440(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26d6fea80a0012e31745f4fbd41a349358e33bd06a4fa94b8544e62e5924483(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d323e4fc31c021ed4aa893cfda96d84da5da2841f2e7f467fe3eacaaca7a20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsDotNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5594627fb39ae6c7bd8b57a9d4796e81781fa4e9d86c0e928dc3a1babc1a0c40(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33b541e948ccd35770dbeae34db81e7a02abd27880205abf137f5d54e1b5222(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1c7bcdf31e7df8d9a74815ee81ae97a7f11cdb2b6d92c911995d3786d2d5c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsDotNetworks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87392312e5126b15cdfbc2a9954e2ccd1ad5a76895e4f201d38ba1b270184e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6feeca862dd6ed4020d14efcc59b37295104aa450259d40ce91738e62f87607d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsDotNetworks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e817f8a91f992b515ef1742cce88309f2f32b7f10861c9918a38427608c2940(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cac9bc7c649673e6f49417e43a18fced3ed21cc814186692c9c21973bd1bd41(
    value: typing.Optional[TeamsLocationEndpointsDot],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f975412f2fd57af9064a053a77baf6b52b080cddc3633fb93b44982445684426(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ffe42f83e5a999f9931b68c11e787e553e29586cb1fc9b5e53ed18cb4b1109(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e86cb3cd5b20334762d0fed93e7bed947743e69827e3d5c569faa36b43f9f1b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849034eab0ef8f0e9dc58c8040e3c3e68805b1d38718d198b9f2256bc8264e99(
    value: typing.Optional[TeamsLocationEndpointsIpv4],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2640b35b7873e07c662dbccdd83e270ac611dcc4f774bc8025564da1eaf654f4(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    networks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsIpv6Networks, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7958f8df7d0a929a33ecd6ba03ef94464a086657e9b635e5de41b83bd5659c9(
    *,
    network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49cb877245be38aa209f769176875c83971862fafd94cf4e6464183eb367b6fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68d7a5a2b0012103b03d13c031fe34b58cda0b5668083906f2ee06d271d0e86(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006b3485263ca290a2313fd6857da44b08c1b4213bd794e8bcf61017d16678ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb0c5e4760782627ef74d260d623c00fe8fb5cd7b0652388db4833adc1c82d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf7469c5299f63db89e3d5ccd9528b4a7c82406693283c8470fa9e618bcc1ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c51d3fb7bff81a30f973886c7a2ab90e14d74b4cc160e0c1f8b14c0494e086b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationEndpointsIpv6Networks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68379f8d4942e5679c83a9dbe6c7a88b6f5c647f102a08400322020e361856c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08367eab72669c7c06c90643650248cb0ee7e7caa62c711b91f0411478c1c19c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20e4f26b40cbe8a6af84c3b01b8b9cd9225588c4de1c974884eb5abea8f9b6f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationEndpointsIpv6Networks]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422308ad23ff41661760b53a8186c7ad30c33e18ca51bd7a3d87187e8ae4be0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2abf56686cffb006b4c464645b81601b1cb0a66cff96262e2787c71bff7e284f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TeamsLocationEndpointsIpv6Networks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09be9738a22d05fd63c84b2f08c81283339bd8eb27eae5f2f315d91e42f4e0da(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abcb1c6f467ee0edc6ccd04c5bbeed123f04de8a53e209abf695e8cb7a19f4c7(
    value: typing.Optional[TeamsLocationEndpointsIpv6],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a08354d562a024fb28f1d3f9f8f74cf1b3245732b254e6f187d227d0ee97de0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1087c877a7d4e10434ec78e808d8f354f793da13ed5f2461127d42c8d64cef(
    value: typing.Optional[TeamsLocationEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119298ce4f1f5f2ee974235314ad6a44be7dbd1e03653c41eff32095695b7063(
    *,
    network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4633e12d4db1c02144181f742e66a4d7b1b43f49c3fbd3c9f4fe0e62518887ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e01cebb75bccd7fba0eb901d5d23069e3af44dc4f51a94bd42f2b3541fd779(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b06c0325d260d7fa6a93961088691afee5aeeb4350cd96e7867592684fd2036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f791d6b48489de48161c3ac50ccda88d65fef6689b213633fb4122e21e7436d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976d5af6336e435d08000145df43747402ad1655c353380f8f165d67e4169141(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b21fd78987a2675fb766f37b3bfbd527f93b770475319d4da367e1f8a76e76a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TeamsLocationNetworks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21eb7ae4952afcc3048e399457e2202645a763f2edf5acca3cb121dadf41afcd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74629982ab28d987e2095f81cbbd2348962076b71f8d2e7b12383956dc336ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea7ba25821cec48d0cc47723f962462657010c4faff98ad2cf66695d8d4ebce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, TeamsLocationNetworks]],
) -> None:
    """Type checking stubs"""
    pass
