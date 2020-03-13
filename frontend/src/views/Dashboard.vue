<template>
  <div>
    <div class="your_booking_box">
      <div class="slot_box">
        <h3 class="slot_box_title">Your booking</h3>
        <div class="slot_box_container">
          <div class="slot_box_content" v-for="booking in bookings" :key="booking.id">
            <p>title: {{booking.title}}</p>
            <p>date: {{booking.start_time}}, capacity: {{booking.reserved}}/{{booking.capacity}}</p>
            <p>detail: {{booking.description}}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="your_booking_box">
      <div class="slot_box">
        <h3 class="slot_box_title">Upcomings</h3>
        <div class="slot_box_container">
          <div class="slot_box_content" v-for="upcoming in upcomings" :key="upcoming.id">
            <p>title: {{upcoming.title}}</p>
            <p>date: {{upcoming.start_time}}, capacity: {{upcoming.reserved}}/{{upcoming.capacity}}</p>
            <p>detail: {{upcoming.description}}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Dashboard',
  data() {
    return {
      upcomings: [
        {
          'id': 1,
          'title': 'Yakiniku',
          'description': 'go to yakiniku',
          'start_time': '2020-03-10',
          'capacity': 5,
          'reserved': 2,
        },
        {
          'id': 2,
          'title': 'Dinner',
          'description': 'dinner',
          'start_time': '2020-03-12',
          'capacity': 1,
          'reserved': 0,
        }
      ],
      bookings: [
        {
        'id': 1,
        'title': 'Yakiniku',
        'description': 'go to yakiniku',
        'start_time': '2020-03-10',
        'capacity': 5,
        'reserved': 2,
      },
      {
        'id': 2,
        'title': 'Dinner',
        'description': 'dinner',
        'start_time': '2020-03-12',
        'capacity': 1,
        'reserved': 0,
      }
    ],
    }
  },
  components: {
  },
  methods: {
  },
  created() {
  }
}
</script>

<style>
  .slot_box {
    text-align: left;
  }
  .slot_box_title {
    padding: 10px;
    background-color: #ececec;
    margin-bottom: 0px;
  }
  .slot_box_container {
    padding: 10px;
  }
  .slot_box_content {
    border-bottom: 1px solid #ccc;
  }
  .slot_box_content > p {
    margin: 4px;
  }
</style>