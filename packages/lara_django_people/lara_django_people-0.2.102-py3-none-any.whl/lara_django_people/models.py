"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_people models *

:details: lara_django_people database models.
         -
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: - remove unwanted models/fields
________________________________________________________________________
"""

import datetime
import hashlib
import json
import logging
import uuid
from random import randint

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from lara_django_base.lara_color_schemes import ColorBlind16
from lara_django_base.models import Address
from lara_django_base.models import CalendarAbstr
from lara_django_base.models import ExtraDataAbstr
from lara_django_base.models import Namespace
from lara_django_base.models import Room
from lara_django_base.models import Tag

settings.FIXTURES += ["2_entitiy_roles_fix", "4_entity_class_fix"]


class ExtraData(ExtraDataAbstr):
    """
    This class can be used to extend data, by extra information,
    e.g., more telephone numbers, customer numbers, ...
    """

    model_curi = "lara:people/ExtraData"
    file = models.FileField(upload_to="people", blank=True, null=True, help_text="rel. path/filename")
    image = models.ImageField(
        upload_to="people/images/",
        blank=True,
        null=True,
        help_text="location room map rel. path/filename to image",
    )
    office_room = models.ForeignKey(
        Room,
        related_name="%(app_label)s_%(class)s_office_room_related",
        related_query_name="%(app_label)s_%(class)s_office_room_related_query",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="extra office",
    )
    laboratory = models.ForeignKey(
        Room,
        related_name="%(app_label)s_%(class)s_laboratory_related",
        related_query_name="%(app_label)s_%(class)s_laboratory_related_query",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="extra laboratory",
    )
    email = models.EmailField(blank=True, null=True, help_text="extra email")

    def save(self, *args, **kwargs):
        """
        Here we generate some default values for name_full
        """
        if self.version is None or self.version == "":
            self.version = "v0.0.1"
        if self.hash_sha256 is None:
            if self.data_json is not None:
                to_hash = json.dumps(self.data_json) + str(self.extradata_id)
                self.hash_sha256 = hashlib.sha256(to_hash.encode("utf-8")).hexdigest()
            else:
                self.hash_sha256 = hashlib.sha256(str(self.extradata_id).encode("utf-8")).hexdigest()

        if self.name is None or self.name == "":
            if self.name_display is None or self.name_display == "":
                self.name = "_".join(
                    (
                        timezone.now().strftime("%Y%m%d_%H%M%S"),
                        "data",
                        self.hash_sha256[:8],
                    )
                )
            else:
                self.name = self.name_display.replace(" ", "_").lower().strip()

        else:
            self.name = self.name.replace(" ", "_").lower().strip()
        if self.name_full is None or self.name_full == "":
            if self.namespace is not None and self.version is not None:
                self.name_full = f"{self.namespace.uri}/" + "_".join((self.name.replace(" ", "_"), self.version))
            else:
                self.name_full = "_".join((self.name.replace(" ", "_"), self.version))

        if not self.iri:
            netloc = self.namespace.parse_URI().netloc
            path = self.namespace.parse_URI().path

            self.iri = f"{settings.LARA_PREFIXES['lara']}people/ExtraData/{netloc}{path}/{self.name.replace(' ', '_').lower().strip()}"

        super().save(*args, **kwargs)


class EntityClass(models.Model):
    """
    Entity class, like university, institute, company, organisation,
    but also guest_scientist, bachelor student, master, postdoc, group leader.
    """

    model_curi = "lara:people/EntityClass"
    entityclass_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(unique=True, help_text="entity class, like university, institute, company, organisation")
    iri = models.URLField(
        blank=True,
        null=True,
        unique=True,
        max_length=512,
        help_text="International Resource Identifier - IRI: is used for semantic representation ",
    )
    description = models.TextField(blank=True, help_text="description of the entity class")

    class Meta:
        verbose_name_plural = "EntityClasses"

    def __str__(self):
        return self.name or ""

    def __repr__(self):
        return self.name or ""

    def save(self, *args, **kwargs):
        """
        Here we generate some default values for IRI
        """
        if self.iri is None or self.iri == "":
            self.iri = (
                f"{settings.LARA_PREFIXES['lara']}people/EntityClass/{self.name.replace(' ', '_').lower().strip()}"
            )

        super().save(*args, **kwargs)


class EntityRole(models.Model):
    """
    Entity role, like scientist, reviewer, developer, maintainer, student, postdoc, project leader, ...
    - remark: the CRedIT taxonomy (https://credit.niso.org/) could be used as an inspiration for roles
    """

    model_curi = "lara:people/EntityRole"
    entityrole_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(
        unique=True, help_text="entity role, like guest_scientist,  bachelor student, master, postdoc, ..."
    )
    iri = models.URLField(
        blank=True,
        null=True,
        unique=True,
        max_length=512,
        help_text="International Resource Identifier - IRI: is used for semantic representation ",
    )
    description = models.TextField(blank=True, null=True, help_text="description of the entity role")

    class Meta:
        verbose_name_plural = "EntityRoles"

    def __str__(self):
        return self.name or ""

    def save(self, *args, **kwargs):
        """
        Here we generate some default values for IRI
        """
        if self.iri is None or self.iri == "":
            self.iri = (
                f"{settings.LARA_PREFIXES['lara']}people/EntityRole/{self.name.replace(' ', '_').lower().strip()}"
            )

        super().save(*args, **kwargs)


class Entity(models.Model):
    """
    Generic Entity Model. An Entity could be, e.g., a person or institution or company.
    The term "entity" encounters for this generalisation.
    """

    class GenderChoices(models.TextChoices):
        GENDER_MALE = "m", _("male")
        GENDER_FEMALE = "f", _("female")
        GENDER_NOT_SPECIFIED = "n", _("not specified")

    class TitleChoices(models.TextChoices):
        DR = "Dr.", _("Doctor")
        PHD = "PhD", _("Doctor of Philosophy")
        DRN = "Dr. rer. nat.", _("Doctor rerum naturalium")
        DRING = "Dr.-Ing.", _("Doctor-Ingenieur")
        DRMED = "Dr. med.", _("Doctor medicinae")
        PROF = "Prof.", _("Professor")
        PRDR = "Prof. Dr.", _("Professor Doctor")
        MR = "Mr.", _("Mister")
        MS = "Ms.", _("Miss")
        MRS = "Mrs.", _("Misses")
        MA = "M.A.", _("Master of Arts")
        MSC = "M.Sc.", _("Master of Science")
        BSC = "B.Sc.", _("Bachelor of Science")
        BA = "B.A.", _("Bachelor of Arts")
        NOTSPEC = "n", _("not specified")

    model_curi = "lara:people/Entity"
    entity_id = models.UUIDField(primary_key=True, editable=False)
    slug = models.SlugField(
        max_length=256,
        blank=True,
        null=True,
        unique=True,
        help_text="slugs are used to display the entity in, e.g. URIs, auto generated, do not use any special characters",
    )  # unique generation does not work with fixtures !
    entity_class = models.ForeignKey(
        EntityClass,
        related_name="%(app_label)s_%(class)s_names_related",
        related_query_name="%(app_label)s_%(class)s_names_related_query",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="class/type/position of the entity, e.g., university, institute, company",
    )
    gender = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        choices=GenderChoices.choices,
    )
    title = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        choices=TitleChoices.choices,
        help_text="title of the person, e.g. Dr., Prof., Mr., Ms., ...",
    )
    name_first = models.TextField(blank=True, help_text="first name of a person or name of an institution/company")
    names_middle = models.TextField(
        blank=True,
        null=True,
        help_text="list of middle names separated by space, e.g. Alfred Ernst Walter Neumann -> Ernst Walter",
    )
    name_last = models.TextField(
        null=True,
        blank=True,
        help_text="last name, e.g. vonSydow - aristocratic prepositions are part of the last name",
    )
    name_full = models.TextField(
        blank=True,
        help_text="full name, e.g. University of Greifswald, Institute for Biochemistry, Max vonSydow, is auto-generated when saved",
    )
    names_last_previous = models.TextField(
        blank=True,
        null=True,
        help_text="list of previous last names separated by space, e.g. changed after marriage, order: latest -> earliest",
    )
    name_nick = models.TextField(blank=True, null=True, help_text="the entities nickname, e.g., James -> Jim.")
    acronym = models.TextField(
        blank=True,
        null=True,
        help_text="3 letter code, autogenerated, should be unique with an institution, could also be used for company acronyms",
    )
    # "uniquness should be only within one institution"
    url = models.URLField(blank=True, null=True, help_text="Universal Resource Locator - URL, web address of entity")
    pid = models.URLField(blank=True, null=True, unique=True, help_text="handle URI")
    # PAC-ID:  https://github.com/ApiniLabs/PAC-ID
    pac_id = models.URLField(
        blank=True,
        null=True,
        unique=True,
        help_text="Publicly Addressable Content IDentifier is a globally unique identifier that operates independently of a central registry.",
    )
    iri = models.URLField(
        blank=True,
        null=True,
        unique=True,
        help_text="International Resource Identifier - IRI: is used for semantic representation ",
    )
    orcid = models.TextField(
        blank=True,
        null=True,
        unique=True,
        help_text="ORCID is a unique researcher ID (just the ID, not the URL), s. https://orcid.org/",
    )  # if person has no ORCID, the system should point to make one
    ror = models.TextField(
        blank=True,
        null=True,
        unique=True,
        help_text="ROR - Research Organization Registry s. https: // ror.readme.io/docs/ror-basics",
    )  # could fetch the address information automatically
    barcode = models.TextField(
        blank=True, null=True, unique=True, help_text="text representation of a barcode of the sample."
    )
    barcode_json = models.JSONField(
        blank=True,
        null=True,
        help_text="Advanced barcodes in JSON for multiple barcode representations, like QR codes etc.",
    )
    tax_no = models.TextField(blank=True, null=True, help_text="Tax number")  # unique=True,
    vat_no = models.TextField(blank=True, null=True, help_text="Value Added Tax number")  # unique=True,
    toll_no = models.TextField(blank=True, null=True, help_text="Toll/EORI number")  # unique=True,

    bank_accounts = models.ManyToManyField(
        "EntityBankAccount",
        blank=True,
        related_name="%(app_label)s_%(class)s_bank_accounts_related",
        related_query_name="%(app_label)s_%(class)s_bank_accounts_related_query",
        help_text="expertise/skills/profession, keywords",
    )
    expertise = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="%(app_label)s_%(class)s_expertises_related",
        related_query_name="%(app_label)s_%(class)s_expertises_related_query",
        help_text="expertise/skills/profession, keywords",
    )
    interests_json = models.JSONField(
        blank=True,
        null=True,
        help_text="scientific interests and expertise, keywords with categories, in JSON(-LD) format",
    )
    interests = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="%(app_label)s_%(class)s_interests_related",
        related_query_name="%(app_label)s_%(class)s_interests_related_query",
        help_text="scientific interests, keywords",
    )
    work_topics = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="%(app_label)s_%(class)s_work_topics_related",
        related_query_name="%(app_label)s_%(class)s_work_topics_related_query",
        help_text="work/research topics, keywords, e.g. transaminases, electrochemistry, fuel cell development",
    )
    roles = models.ManyToManyField(
        EntityRole,
        blank=True,
        related_name="%(app_label)s_%(class)s_roles_related",
        related_query_name="%(app_label)s_%(class)s_roles_related_query",
        help_text="roles of the entity, e.g. project leader, postdoc, bachelor student, master student, guest scientist, ...",
    )
    affiliation_current = models.ForeignKey(
        "self",
        related_name="%(app_label)s_%(class)s_affiliations_related",
        related_query_name="%(app_label)s_%(class)s_affiliations_related_query",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="affiliation of the entity",
    )
    affiliation_start = models.DateField(
        null=True, blank=True, help_text="start date at this affiliation, default: date of today"
    )
    affiliation_end = models.DateField(
        null=True, blank=True, help_text="end date at this affiliation, default: 9.9.9999"
    )
    affiliation_previous = models.ManyToManyField("self", blank=True, help_text="previous affiliations of the entity")
    office_room = models.ForeignKey(
        Room,
        related_name="%(app_label)s_%(class)s_office_rooms_related",
        related_query_name="%(app_label)s_%(class)s_office_rooms_related_query",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="office",
    )
    laboratory = models.ForeignKey(
        Room,
        related_name="%(app_label)s_%(class)s_laboratories_related",
        related_query_name="%(app_label)s_%(class)s_laboratories_related_query",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="laboratory",
    )
    # check relation to auth-user email !
    email = models.EmailField(blank=True, null=True, help_text="entity's current official email address")
    email_private = models.EmailField(blank=True, null=True, help_text="entity's email address")
    email_permanent = models.EmailField(blank=True, null=True, help_text="entity's permanents email address")
    website = models.URLField(blank=True, null=True, help_text="entity's website URL")
    phone_number_mobile = models.TextField(
        blank=True,
        null=True,
        help_text="entity's mobile phone number, if possible add the +Country code notation, e.g., +44 3834 420 4411",
    )
    phone_number_office = models.TextField(
        blank=True,
        null=True,
        help_text="entity's office phone number, if possible add the +Country code notation, e.g., +44 3834 420 4411",
    )
    phone_number_lab = models.TextField(
        blank=True,
        null=True,
        help_text="entity's lab phone number, if possible add the +Country code notation,e.g., +44 3834 420 4411",
    )
    phone_number_home = models.TextField(
        blank=True,
        null=True,
        help_text="entity's phone number at home, if possible add the +Country code notation,e.g., +44 3834 420 4411",
    )
    address = models.ForeignKey(
        Address,
        related_name="%(app_label)s_%(class)s_addresses_related",
        related_query_name="%(app_label)s_%(class)s_addresses_related_query",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="reference to an address",
    )
    date_birth = models.DateField(
        blank=True,
        null=True,
        help_text="date of birth of the person, could also be the founding date of an institution.",
    )
    date_death = models.DateField(
        blank=True, null=True, help_text="date of death, could also be the closing date of an institution."
    )
    color = models.TextField(
        blank=True,
        null=True,
        help_text="GUI colour representation of the entity, can be used in calendars, or gui elements",
    )
    icon = models.TextField(blank=True, null=True, help_text="XML/SVG icon/logo/avatar/drawing of the entity")
    image = models.ImageField(
        upload_to="people/", blank=True, null=True, help_text="entity's image, rel. path/filename to image"
    )
    data_extra = models.ManyToManyField(
        ExtraData,
        related_name="%(app_label)s_%(class)s_entities_data_extra_related",
        related_query_name="%(app_label)s_%(class)s_entities_data_extra_related_query",
        blank=True,
        help_text="e.g. ResearcherID, Scopus Author ID, extra laboratories ...",
    )
    datetime_last_modified = models.DateTimeField(
        null=True, blank=True, help_text="date and time when data was last modified"
    )
    remarks = models.TextField(blank=True, null=True, help_text="remarks about the entity")

    search_vector = SearchVectorField(null=True)

    class Meta:
        verbose_name_plural = "Entities"
        constraints = [
            models.UniqueConstraint(
                fields=["name_full", "date_birth"], name="%(app_label)s_%(class)s_unique_name_full_acronym_pid"
            ),
        ]
        indexes = (GinIndex(fields=["search_vector"]),)

    def __str__(self):
        return self.name_full or ""

    def __repr____(self):
        return f"{self.name_full} - [{self.name_last}|{self.name_first}] - ({self.acronym})" or ""

    # def save(self, force_insert=None, using=None): #force_insert=force_insert, using=using
    def save(self, *args, **kwargs):
        """
        Here we generate some default values for full_name, name, acronym
        TODO: checking special characters and Capitalisation
              uniqueness of name-slug ?
        """
        if self.entity_id is None:
            if self.orcid is not None and self.orcid != "":
                self.entity_id = uuid.uuid5(uuid.NAMESPACE_URL, self.orcid.strip())
            elif self.ror is not None and self.ror != "":
                self.entity_id = uuid.uuid5(uuid.NAMESPACE_URL, self.ror.strip())
            else:
                self.entity_id = uuid.uuid4()

        name_first = self.name_first.strip(".,-") if self.name_first else ""
        name_middle = self.names_middle.strip(".,-") if self.names_middle else ""
        name_last = self.name_last.strip(".,-") if self.name_last else ""

        entity_uid = str(self.entity_id).replace("-", "")

        if self.gender is None or self.gender == "":
            self.gender = (self.GenderChoices.GENDER_NOT_SPECIFIED,)

        if not self.name_full or self.name_full == "":
            if name_middle == "":
                self.name_full = " ".join((name_first, name_last))
            else:
                self.name_full = " ".join((name_first, name_middle, name_last))

        if not self.slug:
            self.slug = "-".join((name_first, name_last, entity_uid[:8])).lower()

        if self.orcid == "":
            self.orcid = None  # avoiding unique constraint violation
        if self.ror == "":
            self.ror = None  # avoiding unique constraint violation

        if self.barcode == "" or self.barcode is None:
            self.barcode = f"AUTO_{str(uuid.uuid4())[:8]}"

        # if not self.image:
        #     self.image.save("-".join(self.name_full.split() + [self.orcid]).lower() + ".jpg", None)

        if not self.acronym and self.name_last is not None:
            ' acronym shall consist of first letter of first name and two letters of last name, in upper case ""'
            i = 0
            j = 2

            if len(self.name_last) > 3:
                self.acronym = "".join(self.name_first[i] + self.name_last[:j]).upper()

                # checking for uniqueness of entry
                while Entity.objects.filter(acronym=self.acronym).exists():
                    if i > len(self.name_last) - 1:
                        # ~ self.stderr.write(self.style.ERROR('ERROR: Auto acronym generation - no uniquie acronym can be generated !'))
                        logging.error(
                            f"Auto acronym generation - no uniquie acronym can be generated for Entity [{self.name_first} -{self.name_last}], adding number ... ! "
                        )
                        self.acronym = "".join(
                            (self.name_first[0] + self.name_last[i] + self.name_last[j]) + str(j)
                        ).upper()
                        j += 1
                    else:
                        self.acronym = "".join(self.name_first[0] + self.name_last[i] + self.name_last[j]).upper()

                    if j < len(self.name_last) - 1:
                        j += 1
                    else:
                        i += 1
                        j = i + 1

            elif len(self.name_full) > 3:  # institute or company
                name_list = self.name_full.split()
                while Entity.objects.filter(acronym=self.acronym).exists():
                    j += 1
                    try:
                        if len(name_list) > 2:
                            self.acronym = "".join([initials[i] for initials in name_list]).upper()
                        else:
                            # should be better selected, check, if unique....
                            self.acronym = self.name_full[:j].upper()
                    except Exception as err:
                        logging.exception(f"Could not generate acronym {err}")

        if self.iri is None or self.iri == "":
            unique_entity_name = "_".join((name_first, name_last, entity_uid)).lower().strip()
            self.iri = f"{settings.LARA_PREFIXES['lara']}people/Entity/{unique_entity_name}"
        if self.pid is None or self.pid == "":
            unique_entity_name = "_".join((name_first, name_last, entity_uid)).lower().strip()
            self.pid = (
                # TODO: adjust to new PID system
                f"{settings.LARA_PID_PREFIXES['entity']}/{unique_entity_name}"
            )

        if self.color is None or self.color == "":
            self.color = ColorBlind16.full_color_scheme[randint(0, 16)].get_web()

        if self.affiliation_start is None:
            self.affiliation_start = datetime.date.today()

        if self.affiliation_end is None:
            self.affiliation_end = datetime.date(9999, 9, 9)

        if self.datetime_last_modified is None:
            self.datetime_last_modified = timezone.now()

        super().save(*args, **kwargs)

    def generate_barcode1D(
        self,
        barcode_format="code128",
        barcode_height=50,
        barcode_width=1,
        barcode_quiet_zone=10,
        barcode_human_readable=True,
        barcode_background_color="white",
        barcode_foreground_color="black",
        barcode_font_size=10,
        barcode_font_path=None,
        barcode_text=False,
        barcode_text_distance=5,
        barcode_text_position="bottom",
        output_format="png",
    ):
        """generates a 1D barcode for the entity,
        e.g. for printing on a badge or for scanning
        """

    def generate_barcode2D(
        self,
        barcode_format="qrcode",
        barcode_error_correction="L",
        barcode_box_size=10,
        barcode_border=4,
        barcode_version=None,
        barcode_mask_pattern=None,
        barcode_image_factory=None,
        barcode_background_color="white",
        barcode_foreground_color="black",
        barcode_text=False,
        barcode_text_distance=5,
        output_format="png",
    ):
        """generates a 2D barcode for the entity,
        e.g. for printing on a badge or for scanning
        """


class Group(models.Model):
    """A group is a collection of entities, e.g. a working group, a project group, a group of developers, ..."""

    model_curi = "lara:people/Group"
    group_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    namespace = models.ForeignKey(
        Namespace,
        related_name="%(app_label)s_%(class)s_namespaces_related",
        related_query_name="%(app_label)s_%(class)s_namespaces_related_query",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="namespace of group",
    )
    group_class = models.ForeignKey(
        EntityClass,
        related_name="%(app_label)s_%(class)s_group_class_related",
        related_query_name="%(app_label)s_%(class)s_group_class_related_query",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="class/type/position of the group, e.g., administrators, developers, ...",
    )
    name = models.TextField(help_text="name of group")

    name_full = models.TextField(
        blank=True,
        null=True,
        unique=True,
        help_text="full name, is auto-generated when saved",
    )
    # mind the difference between the Django group and the LARA group - the Django group is used for permissions
    # the LARA group is used for grouping entities, e.g. for a project group
    # this needs to be considered during synchronisation
    django_group = models.ForeignKey(  # this is the Django group
        DjangoGroup,
        related_name="%(app_label)s_%(class)s_django_groups_related",
        related_query_name="%(app_label)s_%(class)s_django_groups_related_query",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Django group",
    )
    members = models.ManyToManyField(
        Entity,
        related_name="%(app_label)s_%(class)s_members_related",
        related_query_name="%(app_label)s_%(class)s_members_related_query",
        blank=True,
        help_text="members of group",
    )
    description = models.TextField(blank=True, null=True, help_text="description of group")
    remarks = models.TextField(blank=True, null=True, help_text="remarks about the group")
    datetime_last_modified = models.DateTimeField(
        blank=True, null=True, help_text="date and time when data was last modified"
    )

    search_vector = SearchVectorField(null=True)

    class Meta:
        verbose_name_plural = "Groups"
        constraints = [
            models.UniqueConstraint(fields=["name", "namespace"], name="%(app_label)s_%(class)s_unique_name_namespace"),
        ]

    def __str__(self):
        return self.name or ""

    def __repr__(self) -> str:
        return self.name or ""

    def save(self, *args, **kwargs):
        """
        Here we generate some default values for full_name
        """
        if self.name_full is None or self.name_full == "":
            if self.namespace is None:
                self.name_full = self.name.replace(" ", "_").strip().lower()
            else:
                self.name_full = f"{self.namespace.uri}/{self.name.replace(' ', '_').strip().lower()}"

        if self.datetime_last_modified is None:
            self.datetime_last_modified = timezone.now()

        super().save(*args, **kwargs)


class EntityBankAccount(models.Model):
    """Bank account of an Entity."""

    model_curi = "lara:people/EntityBankAccount"
    entitybankaccount_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name_account = models.TextField(
        unique=True, null=True, help_text="label/name of bank account - not name of account holder !"
    )
    account_no = models.TextField(
        unique=True, null=True, help_text="Account Number - for flexibility this is a text field"
    )
    iban = models.TextField(unique=True, null=True, help_text="iban of account")
    bic = models.TextField(unique=True, null=True, help_text="bic of account")
    bank = models.ForeignKey(Entity, on_delete=models.CASCADE, blank=True, null=True, help_text="bank entity")
    description = models.TextField(blank=True, null=True, help_text="description/remarks of account")

    data_extra = models.ManyToManyField(
        ExtraData,
        related_name="%(app_label)s_%(class)s_eba_data_extra_related",
        related_query_name="%(app_label)s_%(class)s_eba_data_extra_related_query",
        blank=True,
        help_text="additions to bank account ...",
    )
    datetime_last_modified = models.DateTimeField(
        blank=True, null=True, help_text="date and time when data was last modified"
    )

    class Meta:
        # verbose_name_plural = "EntityBankAccounts"
        constraints = [
            models.UniqueConstraint(
                fields=["account_no", "iban", "bic"], name="%(app_label)s_%(class)s_unique_account_no_iban_bic"
            ),
        ]

    def __str__(self):
        return self.name_account or ""

    def __repr__(self):
        return self.name_account or ""

    def save(self, *args, **kwargs):
        """
        Here we generate some default values for name
        """
        if self.name_account is None or self.name_account == "":
            self.name_account = f"BankAccount_{self.account_no[:8]}"

        if self.datetime_last_modified is None:
            self.datetime_last_modified = timezone.now()

        super().save(*args, **kwargs)


# we put the abstract classes here, because it is very dependent on the Entity and Group model
class ItemSubsetAbstr(models.Model):
    """This abstract class can be used to generate subsets of arbitrary entities.
    It can be used for selections for orders or modelling etc.
    The class is declared here because of the dependency to the Entity model.
    """

    namespace = models.ForeignKey(
        Namespace,
        related_name="%(app_label)s_%(class)s_namespaces_related",
        related_query_name="%(app_label)s_%(class)s_namespaces_related_query",
        on_delete=models.CASCADE,
        blank=True,
        help_text="namespace of the subset",
    )
    name_display = models.TextField(blank=True, help_text="display name of the subset")
    name = models.TextField(blank=True, help_text="name of the subset")

    user = models.ForeignKey(
        Entity,
        related_name="%(app_label)s_%(class)s_users_related",
        related_query_name="%(app_label)s_%(class)s_users_related_query",
        on_delete=models.CASCADE,
        blank=True,
        help_text="user who created the subset",
    )
    group = models.ForeignKey(
        Group,
        related_name="%(app_label)s_%(class)s_groups_related",
        related_query_name="%(app_label)s_%(class)s_groups_related_query",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="group who created the subset",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="%(app_label)s_%(class)s_tags_related",
        related_query_name="%(app_label)s_%(class)s_tags_related_query",
        help_text="tags",
    )
    description = models.TextField(blank=True, null=True, help_text="description of the subset")
    datetime_last_modified = models.DateTimeField(
        null=True, blank=True, help_text="datetime of last modification of the selection"
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=["name", "namespace"], name="%(app_label)s_%(class)s_unique_name_namespace"),
        ]

    def __str__(self):
        return self.name or ""

    def __repr__(self):
        return self.name or ""

    def save(self, *args, **kwargs):
        if self.name_display is None or self.name_display == "":
            self.name_display = "_".join((timezone.now().strftime("%Y%m%d_%H%M%S"), "subset"))

        if self.name is None or self.name == "":
            self.name = self.name_display.replace(" ", "_").lower().strip()

        self.datetime_last_modified = timezone.now()

        super().save(*args, **kwargs)


class EntitiesSubset(ItemSubsetAbstr):
    """Entities subset - a selection of entities, e.g. for orders, projects, ..."""

    model_curi = "lara:people/EntitiesSubset"
    entitysubset_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entities = models.ManyToManyField(
        Entity,
        related_name="%(app_label)s_%(class)s_entities_subset_related",
        related_query_name="%(app_label)s_%(class)s_entities_subset_related_query",
        blank=True,
        help_text="entities in subset",
        through="OrderedEntitiesEntitiesSubset",
    )


class OrderedEntitiesEntitiesSubset(models.Model):
    """Through model for the many-to-many relationship between EntitiesSubset and Entity."""

    orderedentitiesentitiessubset_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity = models.ForeignKey(
        Entity,
        related_name="%(app_label)s_%(class)s_entities_related",
        related_query_name="%(app_label)s_%(class)s_entities_related_query",
        on_delete=models.CASCADE,
        help_text="entity in subset",
    )
    entities_subset = models.ForeignKey(
        EntitiesSubset,
        related_name="%(app_label)s_%(class)s_entities_subsets_related",
        related_query_name="%(app_label)s_%(class)s_entities_subsets_related_query",
        on_delete=models.CASCADE,
        help_text="subset of entities",
    )
    order = models.PositiveIntegerField(help_text="order of entity in subset")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["entity", "entities_subset"], name="%(app_label)s_%(class)s_unique_entity_subset"
            ),
        ]
        ordering = ("order",)


class GroupsSubset(ItemSubsetAbstr):
    """Groups subset - a selection of groups, e.g. for orders, projects, ..."""

    model_curi = "lara:people/GroupsSubset"
    groupsubset_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    groups = models.ManyToManyField(
        Group,
        related_name="%(app_label)s_%(class)s_groups_subset_related",
        related_query_name="%(app_label)s_%(class)s_groups_subset_related_query",
        blank=True,
        help_text="groups in subset",
        through="OrderedGroupsGroupsSubset",
    )


class OrderedGroupsGroupsSubset(models.Model):
    """Through model for the many-to-many relationship between GroupsSubset and Group."""

    orderedgroupsgroupssubset_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        Group,
        related_name="%(app_label)s_%(class)s_groups_related",
        related_query_name="%(app_label)s_%(class)s_groups_related_query",
        on_delete=models.CASCADE,
        help_text="group in subset",
    )
    groups_subset = models.ForeignKey(
        GroupsSubset,
        related_name="%(app_label)s_%(class)s_group_subsets_related",
        related_query_name="%(app_label)s_%(class)s_group_subsets_related_query",
        on_delete=models.CASCADE,
        help_text="subset of groups",
    )

    order = models.PositiveIntegerField(help_text="order of group in subset")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "groups_subset"], name="%(app_label)s_%(class)s_unique_group_subset"
            ),
        ]
        ordering = ("order",)


class LaraUser(AbstractUser):
    """lara user: an extension of the default django user model to cover entity information
    it extends the django.contrib.auth.models AbstractUser model by an Entity.
    It is used for authentication and authorisation in the (local) LARA system.
    """

    model_curi = "lara:people/LaraUser"

    larauser_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    entity = models.ForeignKey(
        Entity,
        related_name="%(app_label)s_%(class)s_entities_related",
        related_query_name="%(app_label)s_%(class)s_entities_related_query",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="related Entity - storing the complete Affiliation info etc.",
    )
    home_screen_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL to the home screen - this is the default screen after login and can be changed by the user",
    )
    home_screen_layout = models.JSONField(blank=True, null=True, help_text="layout = what to see on the home screen")
    namespace_default = models.ForeignKey(
        Namespace,
        related_name="%(app_label)s_%(class)s_namespaces_related",
        related_query_name="%(app_label)s_%(class)s_namespaces_related_query",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="default namespace for the user",
    )
    access_token = models.TextField(blank=True, help_text="LARA-django (API) access token")
    access_control = models.JSONField(blank=True, null=True, help_text="Access control, similar to Linux ACL")
    # email registration
    confirmation_token = models.TextField(blank=True, help_text="LARA-django e-mail confirmation token")
    # this shall be developed, when login strategies are improved
    email_confirmed = models.EmailField(blank=True, help_text="LARA user confirmed e-mail")
    email_recover = models.EmailField(blank=True, help_text="LARA user account recovering e-mail")
    max_logins = models.SmallIntegerField(blank=True, default=9, help_text="max number of logins")
    failed_logins = models.SmallIntegerField(blank=True, default=0, help_text="number of failed login attempts")
    ip_curr_login = models.TextField(blank=True, help_text="IP address of current  login")
    ip_last_login = models.TextField(blank=True, help_text="IP address of last login")
    datetime_confirmed = models.DateTimeField(blank=True, null=True, help_text="datetime of confirmation")
    datetime_confirmation_sent = models.DateTimeField(
        blank=True, null=True, help_text="datetime of confirmation was sent to the user"
    )

    class Meta:
        db_table = "lara_people_lara_user"

    def __str__(self):
        return self.username or ""

    def __repr__(self):
        return self.username  # + f"({self.entity.name_full})"  or ""

    # automatically connecting to related entity (via uuid)

    def save(self, *args, **kwargs):
        # TODO: use ORCID or ROR to generate the ids
        self.entity, created = Entity.objects.get_or_create(
            entity_id=self.larauser_id,
            defaults={
                "entity_id": self.larauser_id,
                "entity_class": EntityClass.objects.get(name="person"),
                "name_first": self.first_name,
                "name_last": self.last_name,
                "email": self.email,
            },
        )

        super().save(*args, **kwargs)

        # # update allauth emailaddress if exists
        # try:
        #     email_address = EmailAddress.objects.get_primary(user)
        #     if email_address.email != user.email:
        #         email_address.email = user.email
        #         email_address.verified = False
        #         email_address.save()
        # except:to
        #     # if allauth emailaddress doesn't exist create one
        #     EmailAddress.objects.create(
        #         user = user,
        #         email = user.email,
        #         primary = True,
        #         verified = False
        #     )

    # def save(self, *args, **kwargs):
    #     if not hasattr(self, "entity"):
    #         if self.email:
    #             self.entity = Entity.objects.filter(email=self.email).first()

    #     if not hasattr(self, "entity"):
    #         self.entity = Entity.objects.filter(name_first__contains=self.first_name, name_last__contains=self.last_name).first()

    #     if not hasattr(self, "entity"):
    #         self.entity = Entity.objects.create(
    #                 name_first=self.first_name,
    #                 name_last=self.last_name,
    #                 email=self.email,
    #             )

    #     super().save(*args, **kwargs)

    def lara_user_uuid(self):
        return

    @property
    def profile_image(self):
        try:
            return self.entity.image.url
        except ValueError as err:
            logging.exception(f"Could not get profile image {err}")
            return f"{settings.STATIC_URL}lara_django_base/icons/LARA_logo.svg"


# TODO: Django Groups shall be used for grouping - please test, if this is enough and no extra LARA groups might be required ... ???


class MeetingCalendar(CalendarAbstr):
    """Meeting Calendar"""

    model_curi = "lara:people/MeetingsCalendar"
    meetingcalendar_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organiser = models.ForeignKey(
        LaraUser,
        related_name="%(app_label)s_%(class)s_organiser_related",
        related_query_name="%(app_label)s_%(class)s_organiser_related_query",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="LARA User, who created the calendar entry",
    )
    attendees = models.ManyToManyField(
        LaraUser,
        related_name="%(app_label)s_%(class)s_attendees_meetings_calendar_related",
        related_query_name="%(app_label)s_%(class)s_attendees_meetings_calendar_related_query",
        blank=True,
        help_text="attendees of the meeting",
    )
