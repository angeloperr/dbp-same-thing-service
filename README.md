# DBpedia Same Thing Service
Microservice that looks up global and local IRIs based on the most recent [DBpedia ID Management](http://dev.dbpedia.org/ID_and_Clustering) release.

Query the DBpedia Same Thing Service with the IRI of a Wikidata or DBpedia entity (more will follow) and it will return the current DBpedia global IRI for the queried IRI and all known "local" IRIs which are considered to be the same thing.
The "local" IRIs for a global ID are the members of the cluster represented/identified by the global ID. The members of a cluster are assigned by the [DBpedia ID Management Cluster algorithm](http://dev.dbpedia.org/ID_and_Clustering) based on transitive closure of `owl:sameAs` links. 

For each local IRI, a corresponding DBpedia singleton ID has been minted. This identifier is also used to represent the cluster in the microservice output. 
This service can be queried with either global, local, or singleton IRIs, and will return the same representation of a cluster in every case.

**Note:** This service is at an early stage of development, and the stability of its API should not be relied on.
As long as we are at [major version zero](https://semver.org/#spec-item-4), improvements will be prioritized over backwards-compatibility.
This is an excellent time to contribute.
Please create a [GitHub issue](https://github.com/dbpedia/dbp-same-thing-service/issues) for any bug report or enhancement request.

## Usage 
You can query the experimental service deployed within the DBpedia Association infrastructure
[https://global.dbpedia.org/same-thing/lookup/?uri=http://www.wikidata.org/entity/Q8087](https://global.dbpedia.org/same-thing/lookup/?uri=http://www.wikidata.org/entity/Q8087) 
 
or setup your local instance based on the latest DBpedia ID Management release. 
The service is accessed with HTTP GET requests, and accepts the `uri` parameter, which may be any global or local IRI.

### Single URI-Cluster Lookup

`curl "http://localhost:8027/lookup/?meta=off&uri=http%3A%2F%2Fwww.wikidata.org%2Fentity%2FQ8087"`
```
{
  "global": "https://global.dbpedia.org/id/4y9Et",
  "locals": [
    "http://www.wikidata.org/entity/Q8087",
    "http://als.dbpedia.org/resource/Geometrie",
    "http://am.dbpedia.org/resource/ጂዎሜትሪ",
    "http://cs.dbpedia.org/resource/Geometrie",
    "http://bpy.dbpedia.org/resource/জ্যামিতি",
    "http://ar.dbpedia.org/resource/هندسة_رياضية",
    "http://br.dbpedia.org/resource/Mentoniezh",
    "http://af.dbpedia.org/resource/Meetkunde",
    ...
  ],
  "cluster": [
    "4y9Et",
    "9RYmj",
    "Cj9qB",
    "DeSed",
    "EAEXc",
    "EFFeW",
    "EsgRc",
    "FVerP",
    ...
  ]
}
```
If this example does not work when running the service locally, after it has fully loaded, check which port is specified in `docker-compose.yml`.

### Multiple URI-Cluster Lookup
It is also possible to lookup clusters for multiple input URIs simultaneously.
To do this, provide the `uris` parameter (instead of `uri`), and repeat it for each input URI.
This changes the output to include multiple clusters under the `uris` key, as the following example shows:

`curl "http://localhost:8027/lookup/?meta=off&uris=http%3A%2F%2Fdbpedia.org%2Fresource%2FDouglas_Adams&uris=http%3A%2F%2Fdbpedia.org%2Fpage%2FNebraska_Cornhuskers_football&uris=http%3A%2F%2Fdbpedia.org%2Fresource%2FFran%25C3%25A7ois_Legault&uris=http%3A%2F%2Fdbpedia.org%2Fresource%2FFran%C3%A7ois_Legault&uris=http%3A%2F%2Fdbpedia.org%2Fpage%2FToys_%2522R%2522_Us&uris=http%3A%2F%2Fdbpedia.org%2Fresource%2FGio_Gonzalez"`
```
{
  "uris": {
    "http://dbpedia.org/resource/Douglas_Adams": {
      "global": "https://global.dbpedia.org/id/3taAh",
      "locals": [
        "http://www.wikidata.org/entity/Q42",
        "http://et.dbpedia.org/resource/Douglas_Adams",
        "http://mrj.dbpedia.org/resource/Адамс,_Дуглас",
        ...
      ],
      "cluster": [
        "3taAh",
        "5AvRJ",
        "5CNwu",
        ...
      ]
    },
    "http://dbpedia.org/page/Nebraska_Cornhuskers_football": {
      "global": "https://global.dbpedia.org/id/4sKM9",
      "locals": [
        "http://www.wikidata.org/entity/Q6984693",
        "http://simple.dbpedia.org/resource/Nebraska_Cornhuskers_football",
        "http://it.dbpedia.org/resource/Nebraska_Cornhuskers_football",
        "http://dbpedia.org/resource/Nebraska_Cornhuskers_football"
      ],
      "cluster": [
        "4sKM9",
        "6Q5Yy",
        "8aoaz",
        "8sFkU"
      ]
    },
    "http://dbpedia.org/resource/Fran%C3%A7ois_Legault": {
      "global": "https://global.dbpedia.org/id/2rv2n",
      "locals": [
        "http://www.wikidata.org/entity/Q3085147",
        "http://ko.dbpedia.org/resource/프랑수아_르고",
        "http://fr.dbpedia.org/resource/François_Legault",
        "http://dbpedia.org/resource/François_Legault",
        "http://pl.dbpedia.org/resource/François_Legault"
      ],
      "cluster": [
        "2rv2n",
        "6Pqk7",
        "6aTnM",
        "6xys7",
        "83poY"
      ]
    },
    "http://dbpedia.org/resource/François_Legault": {
      "global": "https://global.dbpedia.org/id/2rv2n",
      "locals": [
        "http://www.wikidata.org/entity/Q3085147",
        "http://ko.dbpedia.org/resource/프랑수아_르고",
        "http://fr.dbpedia.org/resource/François_Legault",
        "http://dbpedia.org/resource/François_Legault",
        "http://pl.dbpedia.org/resource/François_Legault"
      ],
      "cluster": [
        "2rv2n",
        "6Pqk7",
        "6aTnM",
        "6xys7",
        "83poY"
      ]
    },
    "http://dbpedia.org/page/Toys_%22R%22_Us": {
      "global": "https://global.dbpedia.org/id/4sKpE",
      "locals": [
        "http://www.wikidata.org/entity/Q696334",
        "http://ja.dbpedia.org/resource/トイザらス",
        "http://sv.dbpedia.org/resource/Toys_%22R%22_Us",
        ...
      ],
      "cluster": [
        "4sKpE",
        "5CJuH",
        "5F6iU",
        ...
      ]
    },
    "http://dbpedia.org/resource/Gio_Gonzalez": null
  }
}

```

## Local Deployment
The microservice is shipped as a docker compose setup.

### Requirements
- Installed docker and [Docker Compose](https://docs.docker.com/compose/install/)

### Running from a pre-built docker image
- Download the compose file: `wget https://raw.githubusercontent.com/dbpedia/dbp-same-thing-service/master/docker-compose.yml`
- Run: `docker-compose up`

This will download the latest image and runs two containers: the `loader` and the webserver (`http`).
The port on which the webserver listens is configurable in the compose file.

When running multiple containers in this way, the loading progress can unfortunately not be displayed.
To monitor the progress of the (initial) Global ID snapshot downloading and ingestion, instead run the following:
- `docker-compose run loader`

After the loader is finished, both containers may be run with `docker-compose up`.

### Bulk Loading
The `loader` downloads the latest Global ID release from `downloads.dbpedia.org` and proceeds to load any source files that haven't been loaded yet into the database.
This might take several hours to complete. After all data is loaded, a backup is made and the loader stops running. 

On subsequent restarts of the loader container (e.g. with `docker-compose run loader` or `docker-compose up`) the loader will check if a new snapshot release is available on the download server, remove old cached downloads, and load the new ID release into a fresh database. 

### Update, Maintenance, & Zero Downtime Features

#### Initial loading
To start running, the webserver  (`http` container) waits for the database to initialize. 
Only on the first run, it will have to wait until the source file has been downloaded, and will start listening for requests once the (empty) database has been created. 
While files are being loaded, the service will respond to requests, but will return `404` for any URI that hasn't been loaded yet. 
Output may also be incomplete until the loader is done.

#### Update to a new release
To check if a new dataset is available, use `docker-compose run loader` or simply rerun `docker-compose up`. The  `loader` will discover the new release, download it, and start to create a new database version. The running webserver however, will not be affected during the download and update process. It will keep serving requests from the already existing fully-loaded database, and will not switch to the newer database while it is running. The next time the `http` container is booted it will use the most recent database (which is typically the one that was latest to download).

#### Database backup and restore
By default, old database versions will will be pruned on startup of the `http` container.
A backup is created, however, after a new database has fully loaded from a snapshot.
Backups of the two most recent DBs are kept, to allow restoring the latest full DB, and the previous version.

The latest database is automatically restored by the loader if it has gone missing (e.g. if it was manually deleted).
A simple command-line prompt is available to manually restore a DB from a backup.

To restore from a backup manually:
- `docker-compose run loader python -m same_thing.restore`

This will display an overview of available backups, and asks which backup to restore:

```commandline
  id  key       snapshot    created_at
----  --------  ----------  -------------------------
   5  backup:5  2019.02.28  2019-05-04T14:07:57+00:00
   4  backup:4  2018.11.09  2019-05-04T13:05:51+00:00
   
Which backup would you like to restore?
```

After a backup has been restored, you'll probably want to restart the `http` container.
This is necessary for it to start serving requests from the latest (restored) database.

### Development Setup
In case you would like to modify the behavior of your local instance (by editing python files) or to contribute enhancements to this project, 
you can build your own docker image. In order to do so:
- Clone or fork this repository
- `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up`
- any changes to the webapp code will trigger a live reload

We use [pipenv](https://docs.pipenv.org/) for package management. 
Set up a local python environment by running `pipenv install` from the project root. 
Introduce new dependencies with `pipenv install <package_name>` and ensure that the latest `Pipfile.lock` (generated with `pipenv lock`) is included in the same commit as an updated `Pipfile`.

After making any changes other than to python source files, rebuild the image with `docker-compose -f docker-compose.yml -f docker-compose.dev.yml build`. 
The compose file automatically builds the image if none exists, but will not rebuild after changes when using `docker-compose up`.

## Troubleshooting 

If the pre-compiled version of the embedded RocksDB does not work on your CPU architecture (e.g. virtual machine, or older AMD), 
this is likely due to an optimization that depends on an instruction set which is not available on your CPU. 
To build your own image that runs with production settings, follow these steps:
- Clone this repository
- Run `docker-compose up`

This works because the `docker-compose.override.yml` file is automatically applied, which specifies a local image instead of the one from Docker Hub. 
To rebuild the image, e.g. after updating with `git pull`, run `docker-compose build`.

## License
This work may be used, modified, and distributed under the terms of the Apache 2.0 License. 
See [LICENSE](LICENSE) for the terms and conditions.

## Acknowledgements
The microservice is developed and maintained by Alex Olieman ([@aolieman](https://github.com/aolieman)). 
His work has been supported by [@stamkracht](https://github.com/stamkracht) / [Qollap](https://www.qollap.com) and the University of Amsterdam (under [a grant](https://www.nwo.nl/en/research-and-results/research-projects/i/67/30567.html) from The Netherlands Organisation for Scientific Research).
