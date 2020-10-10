

import utils
from fire_mark import FireMark

if __name__ == "__main__":

    start_print = FireMark(
        utils.printing_option(), utils.quantity(), utils.opacity())
    start_print.watermark_option()

"""   add_watermark(utils.get_path_from_user(),
                  input("Enter watermark: "),
                  utils.percent_to_byte(int(input("Enter opacity percentage: "))), "single")
"""
