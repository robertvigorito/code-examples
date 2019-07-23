import shotgun

from pprint import pprint as pp
import time
sg = shotgun.connect()

ACHIEVED_FIELD = 'project.Project.archived'
EPISODE_FIELD = 'sg_episode.CustomEntity01.code'
PROJECT_FIELD = 'project'
NAME_FIELD = 'name'


def project_dict():
    """
    Get all the project details from shotgun including episode list,
    and project type...
    """

    project_dict = dict()
    sequence_query_list = sg.find('Sequence', [['code', 'is_not', '']], [ACHIEVED_FIELD, NAME_FIELD,
                                                                         PROJECT_FIELD, EPISODE_FIELD])

    for item in sequence_query_list:
        if item.get(ACHIEVED_FIELD) is True:
            continue

        project_name = item.get('project', {}).get('name')
        project_id = item.get('project', {}).get('id')
        episode = item.get(EPISODE_FIELD)

        key = (project_name, project_id)

        if project_dict.get(key, None) is None:
            project_dict[key] = {episode}
        else:
            project_dict[key].add(episode)

    return project_dict


def iter_projects():
    """
    List all projects from shotgun...
    """

    projects = sg.find('Project', [['archived', 'is_not', True]], ['name'])

    for project in projects:
        name = project.get('name')
        yield name


def list_episodes(project):
    """
    List the project episode...
    """

    project = sg.find_one('Project', [['name', 'is', project]], ['code'])
    episode_query = sg.find('CustomEntity01', [['project', 'is', project]], ['code'])

    for episode in episode_query:
        yield episode.get('code')


def list_status():
    """
    Search the shot status field entity to return the status values...
    """

    field = 'sg_status_list'
    status_query = sg.schema_field_read('Shot', field)
    value = status_query[field]['properties']['display_values']['value']

    value = [value.get(key) for key in value ]
    value.sort()

    return value

if __name__ == '__main__':
    start_time = time.time()
    project_dict()

    print 'Total TIme:\t' + str(time.time() - start_time)