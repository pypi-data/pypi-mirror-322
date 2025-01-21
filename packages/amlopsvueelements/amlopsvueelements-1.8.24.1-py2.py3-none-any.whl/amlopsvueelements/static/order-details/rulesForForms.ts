import { email, helpers, required, requiredIf } from '@vuelidate/validators'
import { isIncorrectDate, isValidStatusFuture, isValidStatusPast } from './validation'
import { useOrderFormStore } from '@/stores/useOrderFormStore'
import type { IOrderStatus } from '@/types/order/order.types';

export const rules = () => {
  const { formModel: form } = useOrderFormStore();

  const fuelOrderRules = form?.type?.is_fuel ? {
    arrival_datetime_utc: {
      required,
      arrivalLocationValidation: helpers.withMessage(
        'Arrival Date inconsistency between Arrival and Departure Date',
        (value: Date) => {
          return isIncorrectDate(form.fuel_order!.departure_datetime_utc, value.toString())
        }
      )
    },
    departure_datetime_utc: {
      required,
      departureLocationValidation: helpers.withMessage(
        'Departure Date inconsistency between Arrival and Departure Date',
        (value: Date) => {
          return isIncorrectDate(value.toString(), form?.fuel_order!.arrival_datetime_utc)
        }
      )
    },
    fuel_category: { required },
    fuel_quantity: { required },
    fuel_uom: { required },
    post_pre_minutes: { required },
  } : {};

  const ghOrderRules = form?.type?.is_gh ? {
    mission_type: { required },
    arrival_datetime_utc: {
      required,
      arrivalLocationValidation: helpers.withMessage(
        'Arrival Date inconsistency between Arrival and Departure Date',
        (value: Date) => {
          return isIncorrectDate(form?.gh_order!.departure_datetime_utc, value.toString())
        }
      )
    },
    departure_datetime_utc: {
      required,
      departureLocationValidation: helpers.withMessage(
        'Departure Date inconsistency between Arrival and Departure Date',
        (value: Date) => {
          return isIncorrectDate(value.toString(), form?.gh_order!.arrival_datetime_utc)
        }
      )
    },
    ground_handler: { required },
  } : {};

  return {
    form: {
      status: {
        required,
        statusValidationPast: helpers.withMessage(
          'You are attempting to create a retrospective order type without setting the order status as Confirmed or Done. Please correct the order dates or status and try again.',
          (value: IOrderStatus) => {
            const date = form?.type?.is_fuel ? form.fuel_order?.arrival_datetime_utc : form?.gh_order!.arrival_datetime_utc;
            return isValidStatusPast(date, value.id)
          }
        ),
        statusValidationFuture: helpers.withMessage(
          'You are attempting to create a new future order type that has a status of Done. Please correct the order dates or status and try again.',
          (value: IOrderStatus) => {
            const date = form?.type?.is_fuel ? form.fuel_order?.arrival_datetime_utc : form?.gh_order!.arrival_datetime_utc;
            return isValidStatusFuture(date, value.id)
          }
        )
      },
      type: { required },
      callsign: { required },
      client: { required },
      location: { required },
      operator: { required },
      aircraft: { 
        requiredIf: requiredIf(() => {
          const aircraftType = form.aircraft_type;
          return !aircraftType
        })
      },
      aircraft_type: {
        requiredIf: requiredIf(() => {
          const aircraft = form.aircraft;
          return !aircraft
        })
      },
      destination: {
        requiredIf: requiredIf(() => {
          const destinationIntDom = form.destination_int_dom;
          return !destinationIntDom
        })
      },
      destination_int_dom: {
        requiredIf: requiredIf(() => {
          const destination = form.destination;
          return !destination
        })
      },
      fuel_order: fuelOrderRules,
      gh_order: ghOrderRules,
    }
  }
}

export const personRules = () => {
  return {
    form: {
      details: {
        first_name: { required },
        last_name: { required },
        contact_email: { required, email },
        title: { required },
      },
      jobs: {
        role: { required },
        job_title: { required },
      }
    }
  }
}
