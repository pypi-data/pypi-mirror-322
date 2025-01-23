import numpy as np
import spike2py_reflex as s2pr
import spike2py_preprocess as s2pp


def calculate_outcomes_of_avg(section):
    """Calculate avg reflex and its outcomes

       For each muscle and for each type of extracted reflex (e.g. H-reflex, mMax),
       calculate the mean waveform and the outcomes of this mean waveform.
       If stimulation was given at different intensities, each will have their
       own average waveform and outcomes.

       Returns
       -------
       For single:

        reflexes.avg_waveform[stim_intensity] = s2pr.Single(waveform=avg_reflex_waveform,
                                                            outcomes=all_outcomes,
                                                            background_sd=background_sd)

       For double:

        reflexes.avg_reflex1[stim_intensity] = s2pr.Single(waveform=avg_reflex_waveform[lower_idx1: upper_idx1],
                                                           outcomes=all_outcomes_reflex1,
                                                           background_sd=background_sd)

        reflexes.avg_reflex2[stim_intensity] = s2pr.Single(waveform=avg_reflex_waveform[lower_idx2: upper_idx2],
                                                           outcomes=all_outcomes_reflex2,
                                                           background_sd=background_sd)
       """

    for muscle, reflexes in section.reflexes.items():
        stim_intensities = get_stim_intensities(reflexes)

        if reflexes.type in [s2pr.utils.SINGLE, s2pr.utils.TRAIN]:
            section.reflexes[muscle] = _single_calculate_avg(reflexes, stim_intensities, section.info.section)

        elif reflexes.type == s2pr.utils.DOUBLE:
            info = section.info
            section.reflexes[muscle] = _double_calculate_avg(reflexes, stim_intensities, info)

    return section


def _single_calculate_avg(reflexes, stim_intensities, section_name):
    reflexes.avg_waveform = dict()
    if _no_stim_intensities(stim_intensities):
        reflexes = _get_single_avg(reflexes, stim_intensities, section_name)
    else:
        for stim_intensity in stim_intensities:
            reflexes = _get_single_avg(reflexes, stim_intensity, section_name)
    return reflexes


def _no_stim_intensities(stim_intensities):
    return not stim_intensities


def get_stim_intensities(reflexes):
    stim_intensities = list()
    for reflex in reflexes.reflexes:
        if reflex.stim_intensity:
            stim_intensities.append(reflex.stim_intensity)
    if len(stim_intensities) == 0:
        return None
    return set(stim_intensities)


def _get_single_avg(reflexes, stim_intensity, section_name):

    # Get average waveform
    avg_reflex_waveform = list()
    for reflex in reflexes.reflexes:
        if (reflex.stim_intensity == stim_intensity) or (stim_intensity is None):
            avg_reflex_waveform.append(reflex.waveform)
    avg_reflex_waveform = np.array(avg_reflex_waveform).mean(axis=0)

    # Get values needed to compute outcomes
    x_axis = reflexes.x_axis_extract

    sd_idx_all_stim_times = reflexes.sd_window_idx
    # Get idx windows of all reflexes types (e.g. H-reflex + mMax; or just mMax)
    reflex_win_idx_all = reflexes.reflex_windows_idx[section_name]

    # Compute outcomes for each reflex type
    all_outcomes = dict()
    for reflex_type, reflex_idx_dict in reflex_win_idx_all.items():
        reflex_win_idx = reflex_idx_dict[reflexes.type]
        if reflexes.type == s2pr.utils.SINGLE:
            sd_idx = sd_idx_all_stim_times[reflexes.type]
        else:
            sd_idx = None
        outcomes, background_sd = s2pr.outcomes.get_outcomes_from(avg_reflex_waveform,
                                                         reflex_win_idx,
                                                         sd_idx, x_axis)
        all_outcomes[reflex_type] = outcomes

    if stim_intensity is None:
        stim_intensity = 'no_intensity'
    reflexes.avg_waveform[stim_intensity] = s2pr.reflexes.Single(waveform=avg_reflex_waveform,
                                                        outcomes=all_outcomes,
                                                        background_sd=background_sd)
    return reflexes


def _double_calculate_avg(reflexes, stim_intensities, info):
    reflexes.avg_waveform = dict()
    reflexes.avg_waveform_for_doubles = dict()

    reflexes.avg_reflex1 = dict()
    reflexes.avg_reflex1_for_doubles = dict()

    reflexes.avg_reflex2 = dict()

    if _no_stim_intensities(stim_intensities):
        reflexes = _get_double_avg(reflexes, stim_intensities, info)
    else:
        for stim_intensity in stim_intensities:
            reflexes = _get_double_avg(reflexes, stim_intensity, info)
    return reflexes


def _get_double_avg(reflexes, stim_intensity, info):

    # Get average waveform
    avg_reflex_waveform = list()  # avg of all waveforms (regardless if mix of Single and Double)
    avg_reflex_waveform_for_doubles = list()  # avg of all waveforms, but excluding those that were a Single
    for reflex in reflexes.reflexes:
        if (reflex.stim_intensity == stim_intensity) or (stim_intensity is None):
            avg_reflex_waveform.append(reflex.waveform)
            if reflex.reflex2 is not None:
                # Do not include instances of Singles when computing avg waveform for Doubles
                avg_reflex_waveform_for_doubles.append(reflex.waveform)

    avg_reflex_waveform = np.array(avg_reflex_waveform).mean(axis=0)
    try:
        avg_reflex_waveform_for_doubles = np.array(avg_reflex_waveform_for_doubles).mean(axis=0)
    except TypeError:
        avg_reflex_waveform_for_doubles = list()

    # avg_waveform and avg_waveform_for_doubles are the same if all reflexes were Double
    # If there was a mix of Single and Double:
    #    avg_waveform_for_doubles will be the avg of the waveforms where there was both a reflex 1 and reflex 2
    #    avg_waveform will the avg of all the waveforms; here, the window where reflex 2 is incorrect as it
    #    represents the avg of one or more true reflex 2 and background noise (in the case of Single).
    reflexes.avg_waveform[stim_intensity] = avg_reflex_waveform
    reflexes.avg_waveform_for_doubles[stim_intensity] = avg_reflex_waveform_for_doubles

    # Get values needed to compute outcomes
    x_axis = reflexes.x_axis_extract

    sd_idx_all_stim_times = reflexes.sd_window_idx
    # Get idx windows of all reflexes types (e.g. H-reflex + mMax; or just mMax)
    reflex_win_idx_all = reflexes.reflex_windows_idx[info.section]

    # Compute outcomes for reflex(es)
    all_outcomes_reflex1 = dict()
    all_outcomes_reflex1_for_doubles = dict()
    all_outcomes_reflex2 = dict()

    for reflex_type, reflex_idx_dict in reflex_win_idx_all.items():
        reflex_win_idx = reflex_idx_dict[reflexes.type]
        sd_idx = sd_idx_all_stim_times[reflexes.type]
        # compute outcomes for reflex1 when avg waveform includes all reflexes (i.e. Single and Double)
        outcomes_reflex1, background_sd = s2pr.outcomes.get_outcomes_from(avg_reflex_waveform, reflex_win_idx[0], sd_idx, x_axis)
        all_outcomes_reflex1[reflex_type] = outcomes_reflex1

        # compute outcomes for reflex1 when avg waveform only includes all the Double
        if len(avg_reflex_waveform_for_doubles) != 0:
            outcomes_reflex1_for_doubles, background_sd_for_doubles = s2pr.outcomes.get_outcomes_from(avg_reflex_waveform_for_doubles, reflex_win_idx[0], sd_idx, x_axis)
            all_outcomes_reflex1_for_doubles[reflex_type] = outcomes_reflex1_for_doubles
            if reflex_win_idx[1] is not None:
                outcomes_reflex2, _ = s2pr.outcomes.get_outcomes_from(avg_reflex_waveform_for_doubles,
                                                                      reflex_win_idx[1], sd_idx, x_axis)
                all_outcomes_reflex2[reflex_type] = outcomes_reflex2
        else:
            all_outcomes_reflex1_for_doubles[reflex_type] = None
            all_outcomes_reflex2[reflex_type] = None

    if stim_intensity is None:
        stim_intensity = 'no_intensity'

    idx_double_single_pulse = info.windows.idx_extract.double_single_pulse
    idx_time_zero = s2pp.find_nearest_time_index(x_axis, 0)

    lower_idx1 = idx_time_zero + idx_double_single_pulse[0]
    upper_idx1 = idx_time_zero + idx_double_single_pulse[1]

    idx_time_isi = s2pp.find_nearest_time_index(x_axis, info.windows.double_isi * s2pr.utils.CONVERT_MS_TO_S)

    lower_idx2 = idx_time_isi + idx_double_single_pulse[0]
    upper_idx2 = idx_time_isi + idx_double_single_pulse[1]

    reflexes.avg_reflex1[stim_intensity] = s2pr.reflexes.Single(waveform=avg_reflex_waveform[lower_idx1: upper_idx1],
                                                        outcomes=all_outcomes_reflex1,
                                                        background_sd=background_sd)

    if len(avg_reflex_waveform_for_doubles) != 0:
        reflexes.avg_reflex1_for_doubles[stim_intensity] = s2pr.reflexes.Single(waveform=avg_reflex_waveform_for_doubles[lower_idx1: upper_idx1],
                                                                    outcomes=all_outcomes_reflex1_for_doubles,
                                                                    background_sd=background_sd_for_doubles)

        try:
            reflexes.avg_reflex2[stim_intensity] = s2pr.reflexes.Single(waveform=avg_reflex_waveform_for_doubles[lower_idx2: upper_idx2],
                                                               outcomes=all_outcomes_reflex2,
                                                               background_sd=background_sd_for_doubles)
        except AttributeError:
            pass
    else:
        reflexes.avg_reflex1_for_doubles[stim_intensity] = None
        reflexes.avg_reflex2[stim_intensity] = None
    return reflexes
