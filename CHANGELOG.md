##  [2.18.1](2023-03-10)


### Bug Fixes

* update graph_instance_from_key method ([060efa4](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/060efa43029b9977d98496373d99f2d55edff431))


### Features

* **ingestion:** excel file ingestion ([58e80c3](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/58e80c335c731fd60472e4d4da5d5f2a8cf265d8))



## [2.16.1](https://gitlab.com/igrafx/logpickr/logpickr-sdk/compare/2.16.0...2.16.1) (2022-11-04)


### Bug Fixes

* display process issue in python API ([210d9eb](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/210d9ebc51c42f5bf18d6373376fb51fd6bca7dd))
* fix the filename of whl artifact in .gitlab-ci.yml ([8df30f2](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/8df30f2ff160cc869e3ab5bca86f333408aed78d))
* get Bad Request on column mapping creation ([7e57c1a](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/7e57c1a6d46d06b0ef59d107785ee1e592937b5d))
* post column mapping returns 204 ([4abac43](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/4abac435b3916a3272d11a03d495177dd0f28981))


### Features

* post column mapping returns 204 ([353b8d9](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/353b8d985d1be30c3efa481d8472618d077c5cc6))



# [2.14.0](https://gitlab.com/igrafx/logpickr/logpickr-sdk/compare/2.13.2...2.14.0) (2022-09-13)


### Bug Fixes

* fix the filename of whl artifact in .gitlab-ci.yml ([c5ad6ac](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/c5ad6acbd8cd4e613957d69141394fd989dac2a9))
* missing project in column mapping APIs ([947ada4](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/947ada455fcc0ea352a182fb67608d1e6b6aced1))



# [2.13.0](https://gitlab.com/igrafx/logpickr/logpickr-sdk/compare/2.12.1...2.13.0) (2022-07-19)


### Bug Fixes

* logpickr_sdk path in pages job ([52afd55](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/52afd55e72a40e77f85daac1edc7b4987eb23839))
* logpickr_sdk path in pages job ([62bc995](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/62bc995017279231f84ecd2c7faf391956b7a318))



## [2.12.1](https://gitlab.com/igrafx/logpickr/logpickr-sdk/compare/1ad30c53f64c9bb297bd86b44a094f8d35750834...2.12.1) (2022-07-11)


### Bug Fixes

* **.gitignore:** added some more paths to ignore ([aa1ebd9](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/aa1ebd972ac5eeb17aabbade4aa172f7216ec4a1))
* **.gitlab-ci.yml:** added a missing "r" to a filepath, re: me being a thundering idiot ([48150bd](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/48150bd3fac8360a4af0a34bb4206a86f2c304db))
* **.gitlab-ci.yml:** added stages to make the dependencies work ([38aeea6](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/38aeea63a1a36a3cbfb46978391c521cc1c7f5a6))
* **datasources:** changed connection parameters ([33b6424](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/33b6424c1933828fa89d3aea51897f3fee047223))
* **docs:** added a missing image file ([16a1dad](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/16a1dad218f80846be2bf4e6e7e7494bc752ed30))
* **docs:** attributed the right copyright owner ([26c2c01](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/26c2c0109a67d3a57d5c66c8fac3d9ea4b532ee4))
* **docs:** fixed some code examples that didn't display properly ([6f92f98](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/6f92f98ee3ba3fa3dc2fda5febcaa9856f3dee00))
* **docs:** removed the sarcasm ([e04bb48](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/e04bb483b68a8bcfa7aa19e124ce9acf361c4dfe))
* **graph_instances:** fixed to handle the new kind of json returned by the API ([d4987ae](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/d4987ae4cd6bf82b61bc5249458389158d80467e))
* **graph:** fixed a circular import issue ([cc8d3bb](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/cc8d3bb5bff2033f86ee3aaaeb1a7db285037aa6))
* **graph:** graphinstance parsing now takes in a json dict instead of a json string ([ae6bcee](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/ae6bceeb1c93e86c3245fac8a7fd0c8d85de9369))
* **login:** fixed the realm in the login url, I'd been logging into the wrong realm all along because one of my two brain cells seems to be on holiday ([3352aa3](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/3352aa39246f3f2129deafda4394a6ceed7b2c83))
* **Project:** added an owner attribute to the project to be able to get the token and make requests from within the project ([444e836](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/444e836f27c0982b095473f013955da29659806b))
* **projects:** fixed a possible memory leak in fetching and creating the projects ([775c751](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/775c7510be32ecc817cfb83d91962abb1c71b9cf))
* removed the old docs folder ([5d86837](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/5d86837a39494b255d043bc3fb957fd5441f1bc7))
* **setup:** added graphviz to the dependencies ([ac77814](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/ac7781464ace81f586ff544e530a78a9a1b7e36a))
* **setup:** added the dependency for the sphinx rtd theme ([a8bd1b9](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/a8bd1b9c0ff22fcda067d87bf44b82105431dbf4))
* **test:** added some info and cleared a TODO ([59ff7ad](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/59ff7ad35e6e95bfe6ecc1625ce45656d4491bac))
* **tests:** rewrote a few tests to reflect changes in the class stucture ([f84b2bd](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/f84b2bd5d5c155eaafe2dd7c59bbb2f77509152b))
* **worgroup:** added some empty returns to work as stubs for the tests ([cd66b58](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/cd66b584fad62eae97133093953a22a80c66d1df))
* **workgroup:** added a missing self that turned project_from_id into a class method. Oops. ([7e547f7](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/7e547f771eab6e601fd584a2a60d8dd25cb3e7cc))


### Features

* **datasources:** added a method to see the columns of a datasource ([dc81131](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/dc81131fa89e2501963344c17176fcbcd8ea05a5))
* **datasources:** added the relevant fields to datasources ([e09c0fa](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/e09c0fa080597a81dd04ad027b6afb531fd8ce5f))
* **datasources:** changed the output of Datasource.request to output a pandas Dataframe, and fixed the relevant issues ([d825d88](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/d825d8895f9da833375d118fcf80e097cbd8f892))
* **datasources:** set up the internal structure of datasources and implemented basic SQL requests ([f8266fe](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/f8266fef1b16bdbba45f5016aa93678925cadc10))
* **docs:** created a script to generate the documentation for the package ([c0227ea](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/c0227ea0b4baf913b9ec7c95a68641b9b8497816))
* **docs:** reworked the documentation and .gitlab-ci.yml to make the wheel downloadable from the documentation. ([ea75278](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/ea75278ed13259df636356bcaf79052c4fb63bbc))
* **file:** implemented the file upload through the API ([5046e55](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/5046e557f2bbdb8433cad4919035b2c0aa12d3b5))
* **graph:** added a parser from json to model graph ([a85ea51](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/a85ea5196c6234e1aab2e9403761dcc58f0bc967))
* **graph:** added the tests relevant to the graph.py classes ([14c71ee](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/14c71ee96faf3e5510b11de8cbdc6c79df63639e))
* **graph:** changed the way vertices are displayed to make them colorable and overall better-looking ([7cb45b7](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/7cb45b756f3436ff012d0732fa0ee0a2c1014ad7))
* **graph:** first stage of gateways in graph instances, need to wait for the API to make sure it works ([35fb79d](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/35fb79d4b5c6fa5fb2c633119e387023ab5989dc))
* **graph:** fixed the graph() property to a method so that it can be called with or without gateways ([2add9b7](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/2add9b7bb4fd14f029e6e5454237f66a67353013))
* **graph:** implemented gateways in model graphs ([28173ab](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/28173ab29e14a920929c25a9c8198ff391c56f1d))
* **graph:** implemented graph visualisation with graphviz ([a4e4b2d](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/a4e4b2d125755e06547254929d1e280689b43b2b))
* **graph:** implemented the request and aprsing of graph instances ([6eba44a](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/6eba44aee297d20828fa4b11065e17a3e78484ae))
* **login:** add login function that takes the credentials and fetches the authorization token ([a994aab](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/a994aab2f0b6495d1c8a298281c03ce57eaee2e1))
* **project:** implemented graph request for the projects ([2bc2f80](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/2bc2f806814cacd05a0fe463fbe0cff26e8a952c))
* **requests:** added handling of token expiration in the various requests ([6b7e16a](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/6b7e16a85a5c0334625f90a3fbab9a97e3eafd0f))
* **requests:** added the train-related requests to the projects. Will need to test it out on the dev plateform I guess. ([e4ad356](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/e4ad356ba26a25ee17dd83042f792a31ed484206))
* **sdk:** Add class definition and constructors ([1ad30c5](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/1ad30c53f64c9bb297bd86b44a094f8d35750834))
* **sdk:** importing the module now succesfully imports all classes in top-level namespace ([f0cc32f](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/f0cc32ffd9eef34de3ae9a83910d31b369021692))
* **sdk:** moved the Project class to workgroup.py ([8c19024](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/8c190248255afdf26522adae1809670a8f1d57f2))
* **sphinx:** changed the theme of the docs to rtd and added the __init__ docstrings to the documentation ([dbede9f](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/dbede9fb9f25762fe33642169d253a7462358790))
* **tests:** reworked the tests so that they can be configured with command line arguments ([82c5548](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/82c5548c989574b05c6550cfb3c373b05d43469e))
* **Vertex:** added attributes to the Vertex class to make it easier to handle and nicer to display ([4343fca](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/4343fca29c8820d21ff24bf8a40ff74a254b339a))
* **worgroup:** added the tests relevant to the workgroup.py classes ([40e5f46](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/40e5f466676a141cc5f5e5ce3870356c958103f3))
* **workgroup:** added a quick method to get a project from its id ([a3665c8](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/a3665c89dc9beeb4304418f221b66ca8a05e2dae))
* **workgroup:** added functions to set the API and AUTH url ([b13fe10](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/b13fe100f792ce18a41c78f038833829820d5619))
* **workgroup:** implemented global datasource request ([e83808e](https://gitlab.com/igrafx/logpickr/logpickr-sdk/commit/e83808e47ab3e59cf2990a0b23dc26cdc767bae4))



