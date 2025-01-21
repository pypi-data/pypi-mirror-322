from pycdm import PyCDM
from pycdm.structs import BsdaSettings, FramingType, EbiSettings
from time import sleep
cdm = PyCDM()
cdm.ebi.flash_ota("/tmp/ebi.bin")
cdm.boot_ebi_ota()
sleep(2)
cdm.mark_ebi_ota_as_ok()
cdm.close()
