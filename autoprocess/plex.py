#!/usr/bin/env python3
import logging
import os
from resources.metadata import MediaType
from plexapi.server import PlexServer
from plexapi.library import Library, LibrarySection
from typing import List

MEDIATYPESOURCE = {
    MediaType.Movie: 'movie',
    MediaType.TV: 'show'
}


def refreshPlex(settings, source_type, path=None, logger=None):
    log: logging.Logger = logger or logging.getLogger(__name__)

    host: str = settings.Plex['host']
    port: int = settings.Plex['port']
    token: str = settings.Plex['token']

    log.debug("Host: %s." % host)
    log.debug("Port: %s." % port)
    log.debug("Token: %s." % token)

    plex: PlexServer = None
    try:
        plex = PlexServer("https://" + settings.address + ':' + str(settings.port), settings.token)
    except:
        try:
            plex = PlexServer("http://" + settings.address + ':' + str(settings.port), settings.token)
        except:
            log.exception("Unable to connect to Plex server")
            plex = None

    if plex:
        log.info("Connected to Plex server %s using server settings" % (plex.friendlyName))
        library: Library = plex.library
        sections: List(LibrarySection) = [s for s in library.sections if s.type == MEDIATYPESOURCE.get(source_type)]

        section: LibrarySection
        for section in sections:
            if any(location for location in section.locations if os.path.commonprefix([path, location]) == location):
                section.update(path=path)
                log.debug("Refreshing %s with path %s" % (section.title, path))
