import os
import config
import spydaap
import spydaap.metadata
from spydaap import db

md_cache = spydaap.metadata.MetadataCache(
    spydaap.media_path,
    spydaap.parsers,
)

md_cache.check_all()
md_cache.build()
db.flush()
