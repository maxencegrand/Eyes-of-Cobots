from data_vis import _GET_USER_INFO, _PLOT_TIME, _PLOT_FIXATION_NUMBER, _PLOT_FIXATION_RATIO,\
    _PLOT_FIXATION_DISPERSION, _PLOT_FIXATION_TIME, _PLOT_FIXATION_AVG_TIME, _PLOT_FIXATION_RATIO_TIME,\
    _PLOT_FIXATION_DISPERSION_MM, _PLOT_SURFACE_TIME, _PLOT_FIXATION_DISTANCE, _PLOT_FIXATION_DISTANCE_RATIO,\
    _PLOT_DISTANCE_OVER_TIME
from conf import Users

users = Users()

print("Extracting results ...")
users = Users()
for id in users.get_users_id_list():
    users.print_user_info(id)
    _PLOT_TIME(id)
    _PLOT_SURFACE_TIME(id)
    _PLOT_FIXATION_TIME(id)
    _PLOT_FIXATION_NUMBER(id)
    _PLOT_FIXATION_DISPERSION_MM(id)
    _PLOT_FIXATION_DISTANCE(id)
    _PLOT_FIXATION_DISTANCE_RATIO(id, 16)
    _PLOT_FIXATION_DISTANCE_RATIO(id, 32)
    _PLOT_FIXATION_DISTANCE_RATIO(id, 64)
    _PLOT_DISTANCE_OVER_TIME(id)
print("Done")
